<link rel="stylesheet" type="text/css" href="/static/content/team-card.css" />

% rebase('layout.tpl', title='Our team', year=year)

<div class="title-wrapper">
    <div class="title-card">
        <h3>{{ message }}</h3>
    </div>
</div>

<canvas id="firework-canvas"></canvas>

% rebase('layout.tpl', title=title, year=year)
<div class="team-card-container">
    % for member in members:
        <div class="team-card">
            <img src="{{ member['photo'] }}" alt="Photo of {{ member['nickname'] }}">
            <div class="team-card-body">
            <div class="team-nickname">{{ member['nickname'] }}</div>
            <div class="team-role">{{ member['role'] }}</div>
            <div class="team-comment">{{ member.get('comment', 'No comments') }}</div>
            </div>
        </div>
    % end
</div>

<script src="/static/scripts/our-team-script.js"/>