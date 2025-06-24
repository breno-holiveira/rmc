import streamlit as st
import geopandas as gpd
import pandas as pd
import json

st.set_page_config(page_title="Mapa RMC – Ultra Profissional", layout="wide", page_icon="🗺️")

# Carregar dados
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values('NM_MUN')

df = pd.read_excel('dados_rmc.xlsx').set_index('nome')

features = []
for _, r in gdf.iterrows():
    nm = r["NM_MUN"]
    props = {"name": nm}
    if nm in df.index:
        d = df.loc[nm]
        props.update({
            "pib": d["pib_2021"],
            "perc": d["participacao_rmc"],
            "pcc": d["per_capita_2021"],
            "pop": d["populacao_2022"],
            "area": d["area"],
            "dens": d["densidade_demografica_2022"]
        })
    else:
        props.update({k: None for k in ["pib","perc","pcc","pop","area","dens"]})
    features.append({"type":"Feature","properties":props,"geometry":r.geometry.__geo_interface__})

geo = {"type":"FeatureCollection","features":features}
geojson = json.dumps(geo)

html = f"""
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>RMC – Design Ultra Profissional</title>
<style>
  *,*::before,*::after{{box-sizing:border-box}}
  html,body{{margin:0;padding:0;height:100vh;
    font-family:sans-serif;background:#fafafa;color:#333;
    overflow:hidden}}
  body{{display:grid;
    grid-template: auto 1fr / 300px 1fr 350px;
    gap:24px;padding:24px}}
  header{{
    grid-column:1/-1;
    font-weight:700;font-size:28px;
    color:#2a3f54;border-bottom:1px solid rgba(0,0,0,0.1);
    padding-bottom:8px;
    user-select:none;
  }}

  nav#sb{{grid-area:1/1/3/2;
    background:rgba(255,255,255,0.95);
    border-radius:20px;padding:24px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    display:flex;flex-direction:column;
    }}
  nav#sb>strong{{
    font-size:20px;color:#3a5a76;
    margin-bottom:16px;
  }}
  input#search{{
    padding:10px 14px;
    border:1px solid #ccc;
    border-radius:14px;
    outline:none;
    margin-bottom:16px;
    transition:border 0.3s ease;
  }}
  input#search:focus{{border-color:#80a0c0}}

  #list{{
    flex-grow:1;overflow-y:auto;font-size:15px;
  }}
  #list div{{
    padding:10px 14px;border-radius:14px;
    margin-bottom:8px;
    cursor:pointer;
    transition: background 0.35s, color 0.35s;
  }}
  #list div:hover{{
    background:rgba(128,160,192,0.1);
    color:#2a3f54;
  }}
  #list div.selected{{
    background:#80a0c0;color:#fff;
  }}

  main#map{{
    position:relative;
    border-radius:20px;
    background:rgba(255,255,255,0.95);
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    overflow:hidden;
  }}
  svg{width:100%;height:100vh}

  div.tooltip{{
    position:absolute;
    pointer-events:none;
    padding:6px 12px;
    background:rgba(41,128,185,0.85);
    color:#fff;
    font-size:13px;
    border-radius:14px;
    opacity:0;transition:opacity 0.3s;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
  }}

  aside#info{{
    background:rgba(255,255,255,0.95);
    border-radius:20px;
    padding:28px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    overflow-y:auto;
    font-size:15px;
    display:flex;
    flex-direction:column;
  }}
  aside#info h2{{
    margin:0 0 16px;
    font-size:22px;
    color:#2a3f54;
  }}
  aside#info .row{{
    display:flex;justify-content:space-between;
    margin-bottom:12px;
  }}
  aside#info .row span{font-weight:600}
  aside#info footer{{
    margin-top:auto;
    font-size:13px;
    color:#666;
    opacity:0.7;
    text-align:right;
  }}
  .polygon{{
    fill:rgba(41,128,185,0.15);
    stroke:rgba(41,128,185,0.6);
    stroke-width:1;
    cursor:pointer;
    transition:fill 0.3s,stroke 0.3s;
  }}
  .polygon:hover{{
    fill:rgba(41,128,185,0.3);
  }}
  .polygon.selected{{
    fill:rgba(41,128,185,0.45);
    stroke:rgba(41,128,185,0.9);
    stroke-width:2;
  }}
</style>
</head><body>
<header>RMC – Indicadores Profissionais</header>
<nav id="sb"><strong>Municípios</strong>
<input id="search" placeholder="Buscar..." />
<div id="list" tabindex="0"></div></nav>
<main id="map"><svg aria-hidden="true"></svg><div class="tooltip"></div></main>
<aside id="info"><h2>Selecione um município</h2>
<div class="row"><strong>PIB:</strong><span>-</span></div>
<div class="row"><strong>% RMC:</strong><span>-</span></div>
<div class="row"><strong>Per Capita:</strong><span>-</span></div>
<div class="row"><strong>População:</strong><span>-</span></div>
<div class="row"><strong>Área:</strong><span>-</span></div>
<div class="row"><strong>Densidade:</strong><span>-</span></div>
<footer>Fonte: IBGE Cidades</footer></aside>
<script>
(function(){
  const geo = {geojson};
  const svg = document.querySelector("svg");
  const tooltip = document.querySelector(".tooltip");
  const list = document.getElementById("list");
  const info = document.getElementById("info");
  const search = document.getElementById("search");
  let selected=null;
  const paths={};

  // projetar
  const pts=[];geo.features.forEach(f=>{
    const g=f.geometry;
    (g.type==="Polygon"?[g.coordinates]:g.coordinates)
      .flat().forEach(r=>r.forEach(c=>pts.push(c)));
  });
  const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
  const [minX,maxX]=[Math.min(...xs),Math.max(...xs)];
  const [minY,maxY]=[Math.min(...ys),Math.max(...ys)];

  function proj([x,y]) {
    const px=(x-minX)/(maxX-minX);
    const py=(y-minY)/(maxY-minY);
    return [50+px*900,950-50-py*900];
  }
  function drawPath(coords){
    return coords.map(c=>{
      const [x,y]=proj(c);
      return x+","+y;
    }).join(" ");
  }

  // criar
  geo.features.forEach(f=>{
    const nm=f.properties.name;
    const g=f.geometry;
    const path = document.createElementNS("http://www.w3.org/2000/svg","path");
    path.setAttribute("data-name",nm);
    path.classList.add("polygon");
    if(g.type==="Polygon"){
      path.setAttribute("d","M"+drawPath(g.coordinates[0])+"Z");
    } else {
      path.setAttribute("d",g.coordinates.map(poly=>"M"+drawPath(poly[0])+"Z").join(""));
    }
    svg.append(path);
    paths[nm]=path;

    const itm=document.createElement("div");
    itm.textContent=nm;
    itm.setAttribute("data-name",nm);
    list.append(itm);
  });

  function clearAll(){
    Object.values(paths).forEach(p=>p.classList.remove("selected"));
  }
  function showInfo(data){
    info.querySelector("h2").textContent=data.name;
    const sp=info.querySelectorAll(".row span");
    sp[0].textContent = data.pib?data.pib.toLocaleString('pt-BR'):"-";
    sp[1].textContent = data.perc? (data.perc*100).toFixed(2)+"%":"-";
    sp[2].textContent = data.pcc?data.pcc.toLocaleString('pt-BR'):"-";
    sp[3].textContent = data.pop?data.pop.toLocaleString('pt-BR'):"-";
    sp[4].textContent = data.area?data.area.toFixed(1):"-";
    sp[5].textContent = data.dens?data.dens.toFixed(1):"-";
  }

  svg.addEventListener("mousemove",e=>{
    if(e.target.classList.contains("polygon")){
      const nm=e.target.dataset.name;
      tooltip.textContent=nm;
      tooltip.style.left=e.pageX+10+"px";
      tooltip.style.top=e.pageY+10+"px";
      tooltip.style.opacity="1";
    } else tooltip.style.opacity="0";
  });

  svg.addEventListener("click",e=>{
    if(e.target.classList.contains("polygon")){
      selected=e.target.dataset.name;
      clearAll();
      paths[selected].classList.add("selected");
      list.querySelectorAll("div").forEach(d=>d.classList.toggle("selected",d.dataset.name===selected));
      const feat=geo.features.find(x=>x.properties.name===selected);
      if(feat)showInfo(feat.properties);
    }
  });

  list.addEventListener("click",e=>{
    const d=e.target;
    if(d.dataset.name) d.click();
  });

  search.addEventListener("input",()=>{
    const v=search.value.toLowerCase();
    list.querySelectorAll("div").forEach(d=>{
      const ok=d.textContent.toLowerCase().includes(v);
      d.style.display=ok?"block":"none";
      if(paths[d.dataset.name]) paths[d.dataset.name].style.display=ok?"inline":"none";
    });
  });
})();
</script></body></html>
"""

st.components.v1.html(html, height=900, scrolling=True)
