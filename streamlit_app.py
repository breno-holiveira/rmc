import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Página e título
st.set_page_config(page_title="RMC - Indicadores", layout="wide")
st.title("RMC Data")
st.markdown("### Indicadores detalhados da Região Metropolitana de Campinas")

# Dados geográficos
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
gdf = gdf.sort_values("NM_MUN")

# Dados tabulares
df = pd.read_excel("dados_rmc.xlsx")
df.set_index("nome", inplace=True)

# Construção GeoJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML+CSS+JS - TOTALMENTE REFEITO DO ZERO - DESIGN TOP FINAL
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>RMC Data - The Best</title>

<!-- Fonte Premium: 'IBM Plex Sans' -->
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&display=swap" rel="stylesheet" />

<style>
  /* Reset */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}

  html, body {{
    margin: 0; padding: 0;
    height: 100vh; width: 100vw;
    font-family: 'IBM Plex Sans', sans-serif;
    background: #fafafa;
    color: #242424;
    font-weight: 300;
    font-size: 14px;
    user-select: none;
    display: flex;
    overflow: hidden;
  }}

  /* Sidebar */
  #sidebar {{
    width: 280px;
    background: #ffffff;
    border-right: 1px solid #ddd;
    box-shadow: 4px 0 10px rgba(0,0,0,0.05);
    padding: 32px 24px 24px 24px;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }}

  #sidebar h1 {{
    margin: 0;
    font-weight: 600;
    font-size: 22px;
    color: #1f2937;
    user-select: text;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}

  #sidebar p {{
    margin: 4px 0 16px 0;
    font-weight: 300;
    font-size: 13px;
    color: #475569;
    user-select: text;
  }}

  #search {{
    padding: 12px 16px;
    border: 1.2px solid #cbd5e1;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 300;
    color: #334155;
    outline-offset: 2px;
    transition: border-color 0.3s ease;
  }}

  #search::placeholder {{
    color: #94a3b8;
    font-style: italic;
  }}

  #search:focus {{
    border-color: #2563eb;
    box-shadow: 0 0 8px rgba(37, 99, 235, 0.25);
  }}

  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 12px;
  }}

  #list::-webkit-scrollbar {{
    width: 7px;
  }}

  #list::-webkit-scrollbar-thumb {{
    background-color: #cbd5e1;
    border-radius: 12px;
  }}

  #list div {{
    padding: 10px 14px;
    margin-bottom: 8px;
    border-radius: 12px;
    font-weight: 400;
    font-size: 14px;
    color: #334155;
    cursor: pointer;
    transition: background-color 0.25s ease, color 0.25s ease;
    user-select: none;
    border: 1.5px solid transparent;
  }}

  #list div:hover {{
    background-color: #e0e7ff;
    color: #1e40af;
  }}

  #list div.active {{
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    border-color: #1e3a8a;
  }}

  /* Main container */
  #main {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    border-radius: 0 24px 24px 0;
    padding: 48px 48px 48px 56px;
    box-shadow: inset 0 0 0 1px #e2e8f0;
    position: relative;
  }}

  /* SVG mapa */
  svg {{
    width: 100%;
    height: 100%;
    border-radius: 14px;
    user-select: none;
  }}

  /* Polígonos */
  .area {{
    fill: #cbd5e1;
    stroke: #64748b;
    stroke-width: 1.4;
    cursor: pointer;
    transition: fill 0.3s ease, stroke-width 0.3s ease;
  }}

  .area:hover {{
    fill: #3b82f6;
    stroke-width: 2;
  }}

  .area.selected {{
    fill: #2563eb;
    stroke: #1e40af;
    stroke-width: 2.5;
  }}

  /* Tooltip */
  #tooltip {{
    position: fixed;
    pointer-events: none;
    background: rgba(37, 99, 235, 0.9);
    color: white;
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 400;
    user-select: none;
    white-space: nowrap;
    box-shadow: 0 2px 12px rgba(37, 99, 235, 0.5);
    display: none;
    z-index: 1000;
    transition: opacity 0.3s ease;
  }}

  /* Info box flutuante */
  #info {{
    position: fixed;
    top: 40px;
    right: 40px;
    width: 320px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: saturate(180%) blur(16px);
    border-radius: 24px;
    box-shadow: 0 14px 32px rgba(31, 41, 55, 0.15);
    padding: 28px 32px;
    font-weight: 300;
    font-size: 14px;
    line-height: 1.55;
    color: #334155;
    user-select: text;
    display: none;
    border: 1px solid rgba(148, 163, 184, 0.3);
  }}

  #info.visible {{
    display: block;
  }}

  #info h3 {{
    margin: 0 0 24px 0;
    font-weight: 600;
    font-size: 20px;
    color: #1e293b;
    letter-spacing: 0.03em;
    user-select: text;
  }}

  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px 36px;
  }}

  #info .label {{
    font-weight: 400;
    color: #64748b;
    white-space: nowrap;
    user-select: text;
  }}

  #info .value {{
    font-weight: 600;
    color: #1e293b;
    text-align: right;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    user-select: text;
  }}

  #info .source {{
    grid-column: 1 / -1;
    font-style: italic;
    font-weight: 300;
    font-size: 12px;
    color: #94a3b8;
    margin-top: 36px;
    text-align: right;
    user-select: none;
  }}

  /* Scrollbar do sidebar */
  #list::-webkit-scrollbar {{
    width: 6px;
  }}
  #list::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #list::-webkit-scrollbar-thumb {{
    background-color: #94a3b8;
    border-radius: 10px;
  }}
</style>
</head>
<body>
  <aside id="sidebar" role="complementary" aria-label="Lista de municípios">
    <h1>Municípios RMC</h1>
    <p>Busque e selecione um município para visualizar seus indicadores.</p>
    <input id="search" type="search" placeholder="Buscar município..." aria-label="Buscar município" autocomplete="off" />
    <div id="list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </aside>

  <main id="main" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </main>

  <section id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Município</h3>
    <div class="grid">
      <div class="label">PIB 2021:</div><div class="value" id="pib">-</div>
      <div class="label">% no PIB regional:</div><div class="value" id="part">-</div>
      <div class="label">PIB per capita (2021):</div><div class="value" id="percapita">-</div>
      <div class="label">População (2022):</div><div class="value" id="pop">-</div>
      <div class="label">Área (km²):</div><div class="value" id="area">-</div>
      <div class="label">Densidade demográfica (hab/km²):</div><div class="value" id="dens">-</div>
      <div class="source">Fonte: IBGE Cidades</div>
    </div>
  </section>

<script>
  const geo = {geojson_str};
  const svg = document.querySelector("svg");
  const tooltip = document.getElementById("tooltip");
  const info = document.getElementById("info");
  const list = document.getElementById("list");
  const search = document.getElementById("search");

  let selected = null;
  const paths = {{}};

  // Coleta de todas as coordenadas para projeção
  let coords = [];
  geo.features.forEach(f => {{
    const g = f.geometry;
    if (g.type === "Polygon") {{
      g.coordinates[0].forEach(c => coords.push(c));
    }} else if (g.type === "MultiPolygon") {{
      g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
    }}
  }});

  const lons = coords.map(c => c[0]);
  const lats = coords.map(c => c[1]);
  const minX = Math.min(...lons), maxX = Math.max(...lons);
  const minY = Math.min(...lats), maxY = Math.max(...lats);

  // Projeta coordenadas geo para SVG
  function project([lon, lat]) {{
    const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
    const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
    return [x, y];
  }}

  // Transforma lista de coords em path SVG
  function polygonToPath(coords) {{
    return coords.map(c => project(c).join(",")).join(" ");
  }}

  // Seleciona município e atualiza UI
  function select(name) {{
    if (selected) {{
      paths[selected].classList.remove("selected");
      [...list.children].forEach(d => d.classList.remove("active"));
    }}
    selected = name;
    if (paths[name]) {{
      paths[name].classList.add("selected");
      [...list.children].forEach(div => {{
        if(div.dataset.name === name) {{
          div.classList.add("active");
          const container = list;
          const containerHeight = container.clientHeight;
          const containerTop = container.getBoundingClientRect().top;
          const elementTop = div.getBoundingClientRect().top;
          const elementHeight = div.offsetHeight;
          const scrollTop = container.scrollTop;
          const offset = elementTop - containerTop;
          const scrollTo = scrollTop + offset - containerHeight / 2 + elementHeight / 2;
          container.scrollTo({{ top: scrollTo, behavior: "smooth" }});
        }}
      }});
      showInfo(name);
    }}
  }}

  // Atualiza caixa info
  function showInfo(name) {{
    const f = geo.features.find(f => f.properties.name === name);
    if (!f) return;
    info.querySelector("h3").textContent = name;
    info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
    info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
    info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
    info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
    info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") : "-";
    info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") : "-";
    info.classList.add("visible");
  }}

  // Atualiza lista conforme busca
  function updateList(filter = "") {{
    const filterLower = filter.toLowerCase();
    [...list.children].forEach(div => {{
      div.style.display = div.textContent.toLowerCase().includes(filterLower) ? "block" : "none";
    }});
  }}

  // Cria paths e itens da lista
  geo.features.forEach(f => {{
    const name = f.properties.name;
    let d = "";
    if (f.geometry.type === "Polygon") {{
      d = "M" + polygonToPath(f.geometry.coordinates[0]) + " Z";
    }} else if (f.geometry.type === "MultiPolygon") {{
      f.geometry.coordinates.forEach(p => {{
        d += "M" + polygonToPath(p[0]) + " Z ";
      }});
    }}
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d.trim());
    path.classList.add("area");
    path.setAttribute("data-name", name);
    svg.appendChild(path);
    paths[name] = path;

    path.addEventListener("mousemove", e => {{
      const offsetX = 12;
      const offsetY = -32;
      tooltip.style.left = (e.clientX + offsetX) + "px";
      tooltip.style.top = (e.clientY + offsetY) + "px";
      tooltip.style.display = "block";
      tooltip.textContent = name;
    }});
    path.addEventListener("mouseleave", () => {{
      tooltip.style.display = "none";
    }});
    path.addEventListener("click", e => {{
      e.preventDefault();
      e.stopPropagation();
      select(name);
    }});

    const div = document.createElement("div");
    div.textContent = name;
    div.dataset.name = name;
    div.tabIndex = 0;
    div.setAttribute('role', 'option');
    div.addEventListener("click", () => select(name));
    div.addEventListener("keydown", e => {{
      if (e.key === "Enter" || e.key === " ") {{
        e.preventDefault();
        select(name);
      }}
    }});
    list.appendChild(div);
  }});

  search.addEventListener("input", e => {{
    updateList(e.target.value);
    const visible = [...list.children].filter(d => d.style.display !== "none");
    if (visible.length === 1) {{
      select(visible[0].dataset.name);
    }}
  }});

  // Seleciona primeiro município ao carregar
  if(geo.features.length > 0) {{
    select(geo.features[0].properties.name);
  }}
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700, scrolling=False)
