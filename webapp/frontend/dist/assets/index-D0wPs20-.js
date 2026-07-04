(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))s(o);new MutationObserver(o=>{for(const r of o)if(r.type==="childList")for(const d of r.addedNodes)d.tagName==="LINK"&&d.rel==="modulepreload"&&s(d)}).observe(document,{childList:!0,subtree:!0});function a(o){const r={};return o.integrity&&(r.integrity=o.integrity),o.referrerPolicy&&(r.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?r.credentials="include":o.crossOrigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function s(o){if(o.ep)return;o.ep=!0;const r=a(o);fetch(o.href,r)}})();const M="http://localhost:5000",j={Argentina:"ar",Australia:"au",Austria:"at",Algeria:"dz",Belgium:"be","Bosnia and Herzegovina":"ba",Brazil:"br","Cabo Verde":"cv",Canada:"ca",Colombia:"co","Congo DR":"cd",Croatia:"hr",Curacao:"cw","Czech Republic":"cz",Ecuador:"ec",Egypt:"eg",England:"gb-eng",France:"fr",Germany:"de",Ghana:"gh",Haiti:"ht",Iran:"ir",Iraq:"iq","Ivory Coast":"ci",Japan:"jp",Jordan:"jo","Korea Republic":"kr",Mexico:"mx",Morocco:"ma",Netherlands:"nl","New Zealand":"nz",Norway:"no",Panama:"pa",Paraguay:"py",Portugal:"pt",Qatar:"qa","Saudi Arabia":"sa",Scotland:"gb-sct",Senegal:"sn","South Africa":"za",Spain:"es",Sweden:"se",Switzerland:"ch",Tunisia:"tn",Turkey:"tr",Uruguay:"uy",USA:"us",Uzbekistan:"uz"};function v(t){return t?{USA:"United States","Congo DR":"Democratic Republic of the Congo"}[t]||t:""}function h(t,e=""){const a=j[t];return a?`<img src="https://flagcdn.com/w80/${a}.png" alt="${t}" class="flag-img ${e}" />`:"🏳️"}const n={mode:"random",numSims:1e3,stage:"Winner_prob",confFilter:"ALL",results:[],teams:[],groups:{},jobId:null,polling:null},i=t=>document.getElementById(t),w=i("btn-mode-random"),S=i("btn-mode-scheduled"),l=i("sim-count-slider"),P=i("sim-count-display"),u=i("btn-run-sim"),b=i("run-btn-label"),x=i("sim-progress-wrap"),k=i("progress-bar"),F=i("progress-pct"),N=i("podium"),p=i("results-chart"),A=i("groups-grid"),E=i("teams-grid");function H(){const t=i("bg-canvas"),e=t.getContext("2d");let a,s,o=[];function r(){a=t.width=window.innerWidth,s=t.height=window.innerHeight}function d(){return{x:Math.random()*a,y:Math.random()*s,r:Math.random()*1.5+.3,vx:(Math.random()-.5)*.2,vy:-(Math.random()*.3+.05),alpha:Math.random()*.6+.1,color:Math.random()>.6?"rgba(245,200,66,":Math.random()>.5?"rgba(59,130,246,":"rgba(240,242,255,"}}function I(){r(),o=Array.from({length:120},d)}function $(){e.clearRect(0,0,a,s);for(const c of o)e.beginPath(),e.arc(c.x,c.y,c.r,0,Math.PI*2),e.fillStyle=c.color+c.alpha+")",e.fill(),c.x+=c.vx,c.y+=c.vy,(c.y<-5||c.x<-5||c.x>a+5)&&Object.assign(c,d(),{y:s+5});requestAnimationFrame($)}window.addEventListener("resize",r),I(),$()}function O(){function t(){const e=+l.value;n.numSims=e,P.textContent=e>=1e3?`${(e/1e3).toFixed(e%1e3===0?0:1)}K`:e.toString();const a=(e-+l.min)/(+l.max-+l.min)*100;l.style.setProperty("--pct",a+"%")}l.addEventListener("input",t),t()}function q(){[w,S].forEach(t=>{t.addEventListener("click",()=>{n.mode=t.dataset.mode,w.classList.toggle("active",n.mode==="random"),S.classList.toggle("active",n.mode==="scheduled"),C()})})}function z(){document.querySelectorAll(".stage-tab").forEach(t=>{t.addEventListener("click",()=>{document.querySelectorAll(".stage-tab").forEach(e=>e.classList.remove("active")),t.classList.add("active"),n.stage=t.dataset.stage,y()})})}function R(){document.querySelectorAll(".conf-btn").forEach(t=>{t.addEventListener("click",()=>{document.querySelectorAll(".conf-btn").forEach(e=>e.classList.remove("active")),t.classList.add("active"),n.confFilter=t.dataset.conf,y()})})}function f(t,e="info"){const a=document.createElement("div");a.className=`toast ${e}`,a.textContent=t,document.body.appendChild(a),setTimeout(()=>a.remove(),4e3)}async function m(t,e={}){const a=await fetch(M+t,e);if(!a.ok)throw new Error(`API ${t} → ${a.status}`);return a.json()}async function G(){try{const t=await m("/teams");n.teams=t.teams||[],_()}catch(t){console.warn("teams fetch failed",t)}}async function U(){try{const t=await m("/groups");n.groups=t.groups||{},D()}catch(t){console.warn("groups fetch failed",t)}}async function C(){try{const t=n.mode==="scheduled"?"/results/scheduled":"/results/random",e=await m(t);e.results&&e.results.length&&(n.results=e.results,T(),y())}catch(t){console.warn("results fetch failed",t)}}async function B(){if(!n.jobId){u.disabled=!0,b.textContent="LAUNCHING…",u.classList.add("running"),x.classList.remove("hidden"),L(0);try{const t=await m("/simulate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({mode:n.mode,num_simulations:n.numSims})});n.jobId=t.job_id,b.textContent="SIMULATING…",W()}catch{f("❌ Failed to start simulation. Is the backend running?","error"),g()}}}function L(t){k.style.width=t+"%",F.textContent=t+"%",document.querySelectorAll(".step").forEach((a,s)=>{a.classList.toggle("active",t>=s*25)})}function W(){n.polling=setInterval(async()=>{try{const t=await m(`/simulate/status/${n.jobId}`);L(t.progress||0),t.status==="done"?(clearInterval(n.polling),n.jobId=null,n.results=t.result||[],L(100),setTimeout(()=>{x.classList.add("hidden"),g(),T(),y(),f(`✅ Simulation complete! ${n.numSims.toLocaleString()} tournaments run.`,"success")},600)):t.status==="error"&&(clearInterval(n.polling),n.jobId=null,f("❌ Simulation error: "+t.error,"error"),g())}catch{clearInterval(n.polling),n.jobId=null,f("❌ Lost connection to backend.","error"),g()}},800)}function g(){u.disabled=!1,u.classList.remove("running"),b.textContent="RUN SIMULATION"}function T(){const t=n.results.slice(0,3),e=["🥇","🥈","🥉"],a=["rank-1","rank-2","rank-3"];N.innerHTML=t.map((s,o)=>`
    <div class="podium-card ${a[o]} anim-fade-up" style="animation-delay:${o*.12}s">
      <div class="podium-medal">${e[o]}</div>
      <div class="podium-flag">${h(s.Team,"flag-podium")}</div>
      <div class="podium-name">${v(s.Team)}</div>
      <div class="podium-conf">${s.confederation}</div>
      <div class="podium-prob">${(s.Winner_prob*100).toFixed(1)}%</div>
      <div class="podium-prob-lbl">Win Probability</div>
    </div>
  `).join("")}function y(){let t=[...n.results];if(n.confFilter!=="ALL"&&(t=t.filter(a=>a.confederation===n.confFilter)),t.sort((a,s)=>(s[n.stage]||0)-(a[n.stage]||0)),!t.length){p.innerHTML=`
      <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-text">No teams match this filter.</div>
      </div>`;return}const e=t[0][n.stage]||1;p.innerHTML=t.map((a,s)=>{const o=a[n.stage]||0,r=e>0?o/e*100:0,d=a.confederation||"UEFA";return`
      <div class="chart-row">
        <span class="chart-rank">${s+1}</span>
        <div class="chart-team-info">
          <span class="chart-flag">${h(a.Team,"flag-chart")}</span>
          <div>
            <div class="chart-name">${v(a.Team)}</div>
            <span class="chart-conf-badge conf-${d}">${d}</span>
          </div>
        </div>
        <div class="chart-bar-track">
          <div class="chart-bar bar-${d}" style="width:0%" data-target="${r}"></div>
        </div>
        <span class="chart-pct">${(o*100).toFixed(1)}%</span>
      </div>`}).join(""),requestAnimationFrame(()=>{p.querySelectorAll(".chart-bar").forEach((a,s)=>{setTimeout(()=>{a.style.width=a.dataset.target+"%"},s*25)})})}function D(){const t=Object.entries(n.groups);A.innerHTML=t.map(([e,a])=>`
    <div class="group-card anim-fade-up glass">
      <div class="group-header">
        <span class="group-name">GROUP ${e}</span>
        <span class="group-venue">4 nations</span>
      </div>
      ${a.map(s=>`
        <div class="group-team-row">
          <span class="group-team-flag">${h(s.team,"flag-group")}</span>
          <div class="group-team-info">
            <div class="group-team-name">${v(s.team)}</div>
            <div class="group-team-elo">Elo ${s.elo} · <span class="chart-conf-badge conf-${s.confederation}">${s.confederation}</span></div>
          </div>
          <span class="group-team-strength">${s.strength.toFixed(0)}</span>
        </div>
      `).join("")}
    </div>
  `).join("")}function _(){E.innerHTML=n.teams.map((t,e)=>`
    <div class="team-card anim-fade-up" style="animation-delay:${e%12*.04}s">
      <div class="team-card-flag">${h(t.team,"flag-card")}</div>
      <div class="team-card-rank">#${e+1}</div>
      <div class="team-card-name">${v(t.team)}</div>
      <span class="team-card-conf team-card-conf conf-${t.confederation}">${t.confederation}</span>
      <div class="team-card-stats">
        <div class="team-stat-item">
          <div class="team-stat-val">${t.elo}</div>
          <div class="team-stat-lbl">Elo</div>
        </div>
        <div class="team-stat-item">
          <div class="team-stat-val">${t.strength.toFixed(0)}</div>
          <div class="team-stat-lbl">Strength</div>
        </div>
      </div>
    </div>
  `).join("")}function J(){const t=i("navbar");window.addEventListener("scroll",()=>{t.style.background=window.scrollY>50?"rgba(5,6,15,0.97)":"rgba(5,6,15,0.85)"})}function K(){p.innerHTML=`
    <div class="empty-state">
      <div class="empty-state-icon">⏳</div>
      <div class="empty-state-text">Loading results… (make sure backend is running)</div>
    </div>`,A.innerHTML=Array(12).fill(0).map(()=>'<div class="skeleton" style="height:200px;border-radius:14px;"></div>').join(""),E.innerHTML=Array(12).fill(0).map(()=>'<div class="skeleton" style="height:160px;border-radius:14px;"></div>').join("")}async function Q(){H(),O(),q(),z(),R(),J(),u.addEventListener("click",B),K(),await Promise.all([G(),U(),C()])}Q();
