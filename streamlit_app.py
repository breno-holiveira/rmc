  /* Painel de Informações fixo no mapa */
  #info {
    position: absolute;
    top: 24px;
    right: 24px;
    width: 300px;
    max-height: 85%;
    background: #f0f3f8;
    padding: 16px 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    font-size: 14px;
    line-height: 1.4;
    color: #1a2d5a;
    user-select: none;
    display: none;
    border: 1px solid #d9e2f3;
    z-index: 10;
    overflow-y: auto;
    box-sizing: border-box;
  }
  #info.visible {
    display: block;
  }
  #info h3 {
    margin: 0 0 12px 0;
    font-size: 20px;
    font-weight: 700;
    color: #2c3e70;
    border-bottom: 1px solid #c3d0e8;
    padding-bottom: 6px;
  }
  #info .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 8px;
    column-gap: 20px;
  }
  #info .label {
    font-weight: 600;
    color: #4d648d;
    white-space: nowrap;
  }
  #info .value {
    font-weight: 500;
    text-align: right;
    color: #34495e;
    overflow-wrap: break-word;
  }
  #info .fonte {
    grid-column: 1 / -1;
    font-size: 11px;
    color: #7f8caa;
    font-style: italic;
    margin-top: 16px;
    text-align: right;
  }
