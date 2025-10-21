<template>
  <svg xmlns="http://www.w3.org/2000/svg"
       viewBox="0 0 1440 560"
       preserveAspectRatio="none">
    <g mask="url(#SvgjsMask1022)" fill="none">
        <rect width="1440" height="560" fill="rgba(219,254,221,1)"></rect>
        <path d="M1119.7792397061023 141.02004066641106L1031.223584388857 110.52788322772179 1029.7631758894456 258.6074449229343z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M631.5176929910048 85.03137324936803L653.121412954709 196.1728775485405 764.2629172538814 174.56915758483632 742.6591972901772 63.42765328566384z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M1159.55 303.35 a114.34 114.34 0 1 0 228.68 0 a114.34 114.34 0 1 0 -228.68 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
        <path d="M571.67 492.47 a183 183 0 1 0 366 0 a183 183 0 1 0 -366 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
        <path d="M209.76 138.9 a155.21 155.21 0 1 0 310.42 0 a155.21 155.21 0 1 0 -310.42 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
        <path d="M1219.5663974117845 565.6520023751864L1359.2988720564585 506.33908588187506 1299.9859555631472 366.6066112372009 1160.253480918473 425.9195277305123z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
        <path d="M525.1403472048826 409.6626830435892L625.8327066579826 293.82937388020116 509.99939749459463 193.13701442710112 409.30703804149454 308.97032359048916z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M250.65457520502028 111.15790852200088L247.94477312046257 266.4023659732645 403.1892305717262 269.11216805782226 405.8990326562839 113.8677106065586z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
        <path d="M-149.26 438.28 a182.04 182.04 0 1 0 364.08 0 a182.04 182.04 0 1 0 -364.08 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float1"></path>
        <path d="M1231.87 157.13 a179.96 179.96 0 1 0 359.92 0 a179.96 179.96 0 1 0 -359.92 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float1"></path>
        <path d="M56.88512578693202 126.60362801697934L184.17107193670154 59.08001246807656 78.536350840468-9.519977517118747z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M756.63 377.36 a96.31 96.31 0 1 0 192.62 0 a96.31 96.31 0 1 0 -192.62 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M371.8 224.15 a171.78 171.78 0 1 0 343.56 0 a171.78 171.78 0 1 0 -343.56 0z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float3"></path>
        <path d="M810.3590801940982 405.6672491642019L852.966739467921 501.3656187431891 975.2104641994903 389.6049450429612z" fill="rgba(46, 125, 50, 0.28)" class="triangle-float2"></path>
    </g>

    <defs>
      <mask id="SvgjsMask1022">
        <rect width="1440" height="560" fill="#ffffff"></rect>
      </mask>
    </defs>
  </svg>
</template>

<style scoped>
svg {
  position: fixed;  
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

/* ANIMAÇÕES */
@keyframes float1 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(-10px, 0); }
  100% { transform: translate(0, 0); }
}

@keyframes float2 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(-5px, -5px); }
  100% { transform: translate(0, 0); }
}

@keyframes float3 {
  0% { transform: translate(0, 0); }
  50% { transform: translate(0, -10px); }
  100% { transform: translate(0, 0); }
}

.triangle-float1 { animation: float1 5s infinite; }
.triangle-float2 { animation: float2 4s infinite; }
.triangle-float3 { animation: float3 6s infinite; }
</style>
