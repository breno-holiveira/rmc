<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RMC Data</title>
    <link rel="icon" href="icon.svg" type="image/svg+xml">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f7fc;
        }

        /* Navbar */
        nav {
            background-color: #0B1D3A;
            display: flex;
            justify-content: flex-start;
            padding: 10px;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

        .logo {
            height: 40px;
            margin-right: 15px;
        }

        .navbar-item {
            color: #E0E6F0;
            padding: 14px;
            text-decoration: none;
            display: flex;
            align-items: center;
            transition: background-color 0.3s, color 0.3s;
        }

        .navbar-item:hover {
            background-color: #1F355A;
            color: #FFFFFF;
        }

        .navbar-item.active {
            background-color: #1F355A;
            color: #FFFFFF;
        }

        .main-content {
            margin-top: 60px; /* Adjusted for fixed navbar */
            padding: 20px;
            background-color: #ffffff;
            min-height: 500px;
        }
        
        .hidden {
            display: none;
        }

    </style>
</head>
<body>

    <nav>
        <img src="cubes.svg" alt="Logo" class="logo">
        <a href="#" class="navbar-item active" onclick="changeContent('home')">Início</a>
        <a href="#" class="navbar-item" onclick="changeContent('sobre')">Sobre</a>
        <a href="#" class="navbar-item" onclick="changeContent('economia')">Economia</a>
        <a href="#" class="navbar-item" onclick="changeContent('financas')">Finanças</a>
        <a href="#" class="navbar-item" onclick="changeContent('seguranca')">Segurança</a>
        <a href="https://github.com/breno-holiveira/rmc" class="navbar-item">GitHub</a>
    </nav>

    <div class="main-content">
        <div id="home" class="content-section">Bem-vindo à página inicial do RMC Data.</div>
        <div id="sobre" class="content-section hidden">Aqui você pode aprender mais sobre o projeto.</div>
        <div id="economia" class="content-section hidden">Esta seção aborda a economia.</div>
        <div id="financas" class="content-section hidden">Aqui discutimos sobre finanças.</div>
        <div id="seguranca" class="content-section hidden">A seção de segurança contém as melhores práticas.</div>
    </div>

    <script>
        function changeContent(page) {
            // Esconde todas as seções
            let sections = document.querySelectorAll('.content-section');
            sections.forEach(section => section.classList.add('hidden'));
            
            // Mostra a seção correspondente
            let activeSection = document.getElementById(page);
            if (activeSection) {
                activeSection.classList.remove('hidden');
            }

            // Atualiza a navegação ativa
            let navItems = document.querySelectorAll('.navbar-item');
            navItems.forEach(item => item.classList.remove('active'));
            document.querySelector(`[onclick="changeContent('${page}')"]`).classList.add('active');
        }

        // Inicializa a página com a seção "Início"
        changeContent('home');
    </script>

</body>
</html>
