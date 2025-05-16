<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - GRAFSYS</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/main.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/section.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>
<body>
    <div class="container body-content">
        <div class="header">
            <h1>GRAFSYS Website</h1>
        </div>

        <div class="navbar">
            <a href="/" class="nav-item{{ ' active' if title == 'Home' else '' }}">Home</a>
            <a href="/bfs" class="nav-item{{ ' active' if title == 'BFS' else '' }}">BFS</a>
            <a href="/dfs" class="nav-item{{ ' active' if title == 'DFS' else '' }}">DFS</a>
            <a href="/beam" class="nav-item{{ ' active' if title == 'Beam Search' else '' }}">Beam Search</a>
            <a href="/greedy_coloring" class="nav-item{{ ' active' if title == 'Section 4' else '' }}">Greedy algorithm</a>
            <a href="/our_team" class="nav-item{{ ' active' if title == 'Our team' else '' }}">Our team</a>
        </div>

        {{ !base }}
        <hr />
        <footer>
            <p>&copy; {{ year }} - GRAFSYS - C224</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>