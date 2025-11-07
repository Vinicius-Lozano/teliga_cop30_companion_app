<template>
  <div class="bg-parallax" aria-hidden="true">
    <div class="clouds">
      <span class="cloud" style="--t:12%; --speed:60s;  --scale:1.05; --delay:-30s;"></span>
      <span class="cloud" style="--t:22%; --speed:80s;  --scale:0.95; --delay:-10s;"></span>
      <span class="cloud" style="--t:33%; --speed:70s;  --scale:1.00; --delay:-50s;"></span>
      <span class="cloud" style="--t:18%; --speed:90s;  --scale:1.10; --delay:-70s;"></span>
      <span class="cloud" style="--t:28%; --speed:110s; --scale:1.18; --delay:-90s;"></span>
      <span class="cloud" style="--t:8%;  --speed:75s;  --scale:0.85; --delay:-20s;"></span>
    </div>
    <div class="mountains far"></div>
    <div class="mountains near"></div>
  </div>
</template>

<script setup>
defineOptions({ name: 'BackgroundGlobal' })
</script>

<style>
:root{
  --green-700:#2e7d32; --green-600:#43a047; --green-500:#66bb6a;
  --sky-400:#53a7ff; --sky-300:#6fd0ff;
  --bg:linear-gradient(180deg,var(--sky-400) 0%,var(--sky-300) 45%,#eafff0 100%);
  --ink:#0a1b0d;
}

.bg-parallax{
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: var(--bg);
  overflow: hidden;
}

.clouds{ position:absolute; left:0; right:0; top:0; height:55vh; }
.cloud{
  position:absolute; left:-30vw; top:var(--t,20%);
  width:240px; height:82px; border-radius:50px;
  background: rgba(255,255,255,.92);
  box-shadow:
    -60px 10px 0 10px rgba(255,255,255,.92),
    -20px -6px 0  8px rgba(255,255,255,.92),
     40px  0px 0 10px rgba(255,255,255,.92),
     80px 10px 0  8px rgba(255,255,255,.92);
  filter: blur(0.5px);
  opacity:.78;
  transform: translateX(-30vw) scale(var(--scale,1));
  animation: cloud-drift var(--speed,80s) linear infinite;
  animation-delay: var(--delay,-40s);
}
@keyframes cloud-drift{
  0%   { transform: translateX(-30vw) scale(var(--scale,1)); }
  100% { transform: translateX(130vw) scale(var(--scale,1)); }
}

.mountains{
  position:absolute; left:0; right:0; bottom:0;
  pointer-events:none; will-change: background-position;
}

.mountains.far{
  height:26vh; opacity:.96;
  background-image:
    linear-gradient(to top, rgba(255,255,255,.03), rgba(255,255,255,0) 45%),
    radial-gradient(80px 80px at 40px 100%,  #0b5a39 79px, transparent 80px),
    radial-gradient(68px 68px at 120px 100%, #0b5a39 67px, transparent 68px);
  background-size: 100% 100%, 160px 100%, 160px 100%;
  background-repeat: no-repeat, repeat-x, repeat-x;
  background-position: 0 0, 0 100%, 0 100%;
  animation: forest-far 70s linear infinite;
  filter: saturate(.95);
}

.mountains.near{
  height:23vh; bottom:-1vh; opacity:1;
  background-image:
    linear-gradient(to top, rgba(255,255,255,.06), rgba(255,255,255,0) 45%),
    radial-gradient(100px 100px at 60px 100%,  #0a6e46 99px, transparent 100px),
    radial-gradient(90px  90px  at 160px 100%, #0a6e46 89px, transparent 90px);
  background-size: 100% 100%, 200px 100%, 200px 100%;
  background-repeat: no-repeat, repeat-x, repeat-x;
  background-position: 0 0, 0 100%, 0 100%;
  animation: forest-near 38s linear infinite;
  filter: drop-shadow(0 -6px 18px rgba(0,0,0,.12));
}

@keyframes forest-far  { 0% {background-position:0 0, 0 100%, 0 100%} 100% {background-position:0 0, -160px 100%, -160px 100%} }
@keyframes forest-near { 0% {background-position:0 0, 0 100%, 0 100%} 100% {background-position:0 0, -200px 100%, -200px 100%} }

@media (prefers-reduced-motion: reduce){
  .cloud, .mountains.far, .mountains.near { animation: none !important; }
}
</style>
