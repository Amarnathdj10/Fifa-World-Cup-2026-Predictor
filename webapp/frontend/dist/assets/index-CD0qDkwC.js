(function(){let e=document.createElement(`link`).relList;if(e&&e.supports&&e.supports(`modulepreload`))return;for(let e of document.querySelectorAll(`link[rel="modulepreload"]`))n(e);new MutationObserver(e=>{for(let t of e)if(t.type===`childList`)for(let e of t.addedNodes)e.tagName===`LINK`&&e.rel===`modulepreload`&&n(e)}).observe(document,{childList:!0,subtree:!0});function t(e){let t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin===`use-credentials`?t.credentials=`include`:e.crossOrigin===`anonymous`?t.credentials=`omit`:t.credentials=`same-origin`,t}function n(e){if(e.ep)return;e.ep=!0;let n=t(e);fetch(e.href,n)}})();var e=`https://fifa-world-cup-2026-predictor.onrender.com/api`,t={Argentina:`ar`,Australia:`au`,Austria:`at`,Algeria:`dz`,Belgium:`be`,"Bosnia and Herzegovina":`ba`,Brazil:`br`,"Cabo Verde":`cv`,Canada:`ca`,Colombia:`co`,"Congo DR":`cd`,Croatia:`hr`,Curacao:`cw`,"Czech Republic":`cz`,Ecuador:`ec`,Egypt:`eg`,England:`gb-eng`,France:`fr`,Germany:`de`,Ghana:`gh`,Haiti:`ht`,Iran:`ir`,Iraq:`iq`,"Ivory Coast":`ci`,Japan:`jp`,Jordan:`jo`,"Korea Republic":`kr`,Mexico:`mx`,Morocco:`ma`,Netherlands:`nl`,"New Zealand":`nz`,Norway:`no`,Panama:`pa`,Paraguay:`py`,Portugal:`pt`,Qatar:`qa`,"Saudi Arabia":`sa`,Scotland:`gb-sct`,Senegal:`sn`,"South Africa":`za`,Spain:`es`,Sweden:`se`,Switzerland:`ch`,Tunisia:`tn`,Turkey:`tr`,Uruguay:`uy`,USA:`us`,Uzbekistan:`uz`};function n(e){return e?{USA:`United States`,"Congo DR":`Democratic Republic of the Congo`}[e]||e:``}function r(e,n=``){let r=t[e];return r?`<img src="https://flagcdn.com/w80/${r}.png" alt="${e}" class="flag-img ${n}" />`:`🏳️`}var i={mode:`random`,numSims:1e3,stage:`Winner_prob`,confFilter:`ALL`,results:[],teams:[],groups:{},jobId:null,polling:null,bracket:[],bracketRoundIdx:0},a=e=>document.getElementById(e),o=a(`btn-mode-random`),s=a(`btn-mode-scheduled`),c=a(`sim-count-slider`),l=a(`sim-count-display`),u=a(`btn-run-sim`),d=a(`run-btn-label`),f=a(`sim-progress-wrap`),p=a(`progress-bar`),m=a(`progress-pct`),h=a(`podium`),g=a(`results-chart`),_=a(`groups-grid`),v=a(`teams-grid`),y=a(`bracket-round-tabs`),b=a(`bracket-matches`),x=a(`bracket-prev`),S=a(`bracket-next`);function C(){let e=a(`bg-canvas`),t=e.getContext(`2d`),n,r,i=[];function o(){n=e.width=window.innerWidth,r=e.height=window.innerHeight}function s(){return{x:Math.random()*n,y:Math.random()*r,r:Math.random()*1.5+.3,vx:(Math.random()-.5)*.2,vy:-(Math.random()*.3+.05),alpha:Math.random()*.6+.1,color:Math.random()>.6?`rgba(245,200,66,`:Math.random()>.5?`rgba(59,130,246,`:`rgba(240,242,255,`}}function c(){o(),i=Array.from({length:120},s)}function l(){t.clearRect(0,0,n,r);for(let e of i)t.beginPath(),t.arc(e.x,e.y,e.r,0,Math.PI*2),t.fillStyle=e.color+e.alpha+`)`,t.fill(),e.x+=e.vx,e.y+=e.vy,(e.y<-5||e.x<-5||e.x>n+5)&&Object.assign(e,s(),{y:r+5});requestAnimationFrame(l)}window.addEventListener(`resize`,o),c(),l()}function w(){function e(){let e=+c.value;i.numSims=e,l.textContent=e>=1e3?`${(e/1e3).toFixed(e%1e3==0?0:1)}K`:e.toString();let t=(e-+c.min)/(c.max-+c.min)*100;c.style.setProperty(`--pct`,t+`%`)}c.addEventListener(`input`,e),e()}function T(){[o,s].forEach(e=>{e.addEventListener(`click`,()=>{i.mode=e.dataset.mode,o.classList.toggle(`active`,i.mode===`random`),s.classList.toggle(`active`,i.mode===`scheduled`),M(),N()})})}function E(){document.querySelectorAll(`.stage-tab`).forEach(e=>{e.addEventListener(`click`,()=>{document.querySelectorAll(`.stage-tab`).forEach(e=>e.classList.remove(`active`)),e.classList.add(`active`),i.stage=e.dataset.stage,H()})})}function D(){document.querySelectorAll(`.conf-btn`).forEach(e=>{e.addEventListener(`click`,()=>{document.querySelectorAll(`.conf-btn`).forEach(e=>e.classList.remove(`active`)),e.classList.add(`active`),i.confFilter=e.dataset.conf,H()})})}function O(e,t=`info`){let n=document.createElement(`div`);n.className=`toast ${t}`,n.textContent=e,document.body.appendChild(n),setTimeout(()=>n.remove(),4e3)}async function k(t,n={}){let r=await fetch(e+t,n);if(!r.ok)throw Error(`API ${t} → ${r.status}`);return r.json()}async function A(){try{i.teams=(await k(`/teams`)).teams||[],W()}catch(e){console.warn(`teams fetch failed`,e)}}async function j(){try{i.groups=(await k(`/groups`)).groups||{},U()}catch(e){console.warn(`groups fetch failed`,e)}}async function M(){try{let e=await k(i.mode===`scheduled`?`/results/scheduled`:`/results/random`);e.results&&e.results.length&&(i.results=e.results,V(),H())}catch(e){console.warn(`results fetch failed`,e)}}async function N(){try{i.bracket=(await k(i.mode===`scheduled`?`/bracket/scheduled`:`/bracket/random`)).bracket||[],i.bracketRoundIdx=Math.min(i.bracketRoundIdx,Math.max(0,i.bracket.length-1)),P(),F()}catch(e){console.warn(`bracket fetch failed`,e)}}function P(){if(!i.bracket.length){y.innerHTML=``;return}y.innerHTML=i.bracket.map((e,t)=>`
    <button class="bracket-tab ${t===i.bracketRoundIdx?`active`:``}" data-idx="${t}">${e.round}</button>
  `).join(``),y.querySelectorAll(`.bracket-tab`).forEach(e=>{e.addEventListener(`click`,()=>{i.bracketRoundIdx=+e.dataset.idx,P(),F()})})}function F(){if(!i.bracket.length){b.innerHTML=`
      <div class="empty-state">
        <div class="empty-state-icon">🏆</div>
        <div class="empty-state-text">Run a simulation to generate a bracket.</div>
      </div>`;return}b.innerHTML=i.bracket[i.bracketRoundIdx].matches.map((e,t)=>`
    <div class="bracket-match anim-fade-up" style="animation-delay:${t*.03}s">
      <div class="bracket-team ${e.winner===e.team1?`winner`:``}">
        <span class="bracket-flag">${r(e.team1)}</span>
        <span class="bracket-team-name">${n(e.team1)}</span>
        <span class="bracket-score">${e.score1}</span>
      </div>
      <div class="bracket-team ${e.winner===e.team2?`winner`:``}">
        <span class="bracket-flag">${r(e.team2)}</span>
        <span class="bracket-team-name">${n(e.team2)}</span>
        <span class="bracket-score">${e.score2}</span>
      </div>
    </div>
  `).join(``)}function I(){x.addEventListener(`click`,()=>{i.bracketRoundIdx>0&&(i.bracketRoundIdx--,P(),F())}),S.addEventListener(`click`,()=>{i.bracketRoundIdx<i.bracket.length-1&&(i.bracketRoundIdx++,P(),F())})}async function L(){if(!i.jobId){u.disabled=!0,d.textContent=`LAUNCHING…`,u.classList.add(`running`),f.classList.remove(`hidden`),R(0);try{i.jobId=(await k(`/simulate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({mode:i.mode,num_simulations:i.numSims})})).job_id,d.textContent=`SIMULATING…`,z()}catch{O(`❌ Failed to start simulation. Is the backend running?`,`error`),B()}}}function R(e){p.style.width=e+`%`,m.textContent=e+`%`,document.querySelectorAll(`.step`).forEach((t,n)=>{t.classList.toggle(`active`,e>=n*25)})}function z(){i.polling=setInterval(async()=>{try{let e=await k(`/simulate/status/${i.jobId}`);R(e.progress||0),e.status===`done`?(clearInterval(i.polling),i.jobId=null,i.results=e.result||[],R(100),setTimeout(()=>{f.classList.add(`hidden`),B(),V(),H(),N(),O(`✅ Simulation complete! ${i.numSims.toLocaleString()} tournaments run.`,`success`)},600)):e.status===`error`&&(clearInterval(i.polling),i.jobId=null,O(`❌ Simulation error: `+e.error,`error`),B())}catch{clearInterval(i.polling),i.jobId=null,O(`❌ Lost connection to backend.`,`error`),B()}},800)}function B(){u.disabled=!1,u.classList.remove(`running`),d.textContent=`RUN SIMULATION`}function V(){let e=i.results.slice(0,3),t=[`🥇`,`🥈`,`🥉`],a=[`rank-1`,`rank-2`,`rank-3`];h.innerHTML=e.map((e,i)=>`
    <div class="podium-card ${a[i]} anim-fade-up" style="animation-delay:${i*.12}s">
      <div class="podium-medal">${t[i]}</div>
      <div class="podium-flag">${r(e.Team,`flag-podium`)}</div>
      <div class="podium-name">${n(e.Team)}</div>
      <div class="podium-conf">${e.confederation}</div>
      <div class="podium-prob">${(e.Winner_prob*100).toFixed(1)}%</div>
      <div class="podium-prob-lbl">Win Probability</div>
    </div>
  `).join(``)}function H(){let e=[...i.results];if(i.confFilter!==`ALL`&&(e=e.filter(e=>e.confederation===i.confFilter)),e.sort((e,t)=>(t[i.stage]||0)-(e[i.stage]||0)),!e.length){g.innerHTML=`
      <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-text">No teams match this filter.</div>
      </div>`;return}let t=e[0][i.stage]||1;g.innerHTML=e.map((e,a)=>{let o=e[i.stage]||0,s=t>0?o/t*100:0,c=e.confederation||`UEFA`;return`
      <div class="chart-row">
        <span class="chart-rank">${a+1}</span>
        <div class="chart-team-info">
          <span class="chart-flag">${r(e.Team,`flag-chart`)}</span>
          <div>
            <div class="chart-name">${n(e.Team)}</div>
            <span class="chart-conf-badge conf-${c}">${c}</span>
          </div>
        </div>
        <div class="chart-bar-track">
          <div class="chart-bar bar-${c}" style="width:0%" data-target="${s}"></div>
        </div>
        <span class="chart-pct">${(o*100).toFixed(1)}%</span>
      </div>`}).join(``),requestAnimationFrame(()=>{g.querySelectorAll(`.chart-bar`).forEach((e,t)=>{setTimeout(()=>{e.style.width=e.dataset.target+`%`},t*25)})})}function U(){_.innerHTML=Object.entries(i.groups).map(([e,t])=>`
    <div class="group-card anim-fade-up glass">
      <div class="group-header">
        <span class="group-name">GROUP ${e}</span>
        <span class="group-venue">4 nations</span>
      </div>
      ${t.map(e=>`
        <div class="group-team-row">
          <span class="group-team-flag">${r(e.team,`flag-group`)}</span>
          <div class="group-team-info">
            <div class="group-team-name">${n(e.team)}</div>
            <div class="group-team-elo">Elo ${e.elo} · <span class="chart-conf-badge conf-${e.confederation}">${e.confederation}</span></div>
          </div>
          <span class="group-team-strength">${e.strength.toFixed(0)}</span>
        </div>
      `).join(``)}
    </div>
  `).join(``)}function W(){v.innerHTML=i.teams.map((e,t)=>`
    <div class="team-card anim-fade-up" style="animation-delay:${t%12*.04}s">
      <div class="team-card-flag">${r(e.team,`flag-card`)}</div>
      <div class="team-card-rank">#${t+1}</div>
      <div class="team-card-name">${n(e.team)}</div>
      <span class="team-card-conf team-card-conf conf-${e.confederation}">${e.confederation}</span>
      <div class="team-card-stats">
        <div class="team-stat-item">
          <div class="team-stat-val">${e.elo}</div>
          <div class="team-stat-lbl">Elo</div>
        </div>
        <div class="team-stat-item">
          <div class="team-stat-val">${e.strength.toFixed(0)}</div>
          <div class="team-stat-lbl">Strength</div>
        </div>
      </div>
    </div>
  `).join(``)}function G(){let e=a(`navbar`);window.addEventListener(`scroll`,()=>{e.style.background=window.scrollY>50?`rgba(5,6,15,0.97)`:`rgba(5,6,15,0.85)`})}function K(){g.innerHTML=`
    <div class="empty-state">
      <div class="empty-state-icon">⏳</div>
      <div class="empty-state-text">Loading results… (make sure backend is running)</div>
    </div>`,_.innerHTML=Array(12).fill(0).map(()=>`<div class="skeleton" style="height:200px;border-radius:14px;"></div>`).join(``),v.innerHTML=Array(12).fill(0).map(()=>`<div class="skeleton" style="height:160px;border-radius:14px;"></div>`).join(``)}async function q(){C(),w(),T(),E(),D(),G(),I(),u.addEventListener(`click`,L),K(),await Promise.all([A(),j(),M(),N()])}q();