// Shared object library for the mannequin poser + headless harness.
// An object = { id, name, kind, pos:[x,y,z], rot:[x,y,z] (deg, YXZ), scale:number|[x,y,z], color?:hex, parts?:[...] }
// kind is a LIBRARY entry (stool, chair, table, amp, speaker, mic, wall, box, sphere, cylinder, guitar, spot)
// or 'custom' with parts. A part = { shape, size, pos, rot, color, roughness, metalness }
//   box [w,h,d] | cylinder [rTop,rBottom,h] or [r,h] | sphere [r] | cone [r,h] | capsule [r,len] | plane [w,h] | torus [r,tube]

export const LIBRARY = {
  stool:   { th:'สตูล',     parts: () => [ {shape:'cylinder', size:[0.17,0.17,0.04], pos:[0,0.64,0], color:0x555555},
                              ...[0,1,2,3].map(i => ({shape:'cylinder', size:[0.015,0.015,0.64], pos:[Math.cos(i*Math.PI/2)*0.13,0.32,Math.sin(i*Math.PI/2)*0.13], color:0x555555})) ] },
  chair:   { th:'เก้าอี้',   parts: () => [ {shape:'box', size:[0.42,0.04,0.42], pos:[0,0.45,0], color:0x6b4a2f},
                              {shape:'box', size:[0.42,0.45,0.04], pos:[0,0.69,-0.19], color:0x6b4a2f},
                              ...[[-1,-1],[1,-1],[-1,1],[1,1]].map(([sx,sz]) => ({shape:'cylinder', size:[0.02,0.02,0.45], pos:[sx*0.18,0.225,sz*0.18], color:0x4a3320})) ] },
  table:   { th:'โต๊ะ',     parts: () => [ {shape:'box', size:[1.0,0.04,0.6], pos:[0,0.74,0], color:0x7a5a3a},
                              ...[[-1,-1],[1,-1],[-1,1],[1,1]].map(([sx,sz]) => ({shape:'cylinder', size:[0.025,0.025,0.72], pos:[sx*0.45,0.36,sz*0.25], color:0x4a3320})) ] },
  amp:     { th:'แอมป์',    parts: () => [ {shape:'box', size:[0.6,0.5,0.3], pos:[0,0.25,0], color:0x1e1e1e},
                              {shape:'box', size:[0.52,0.34,0.01], pos:[0,0.2,0.153], color:0x6a5a3a}, {shape:'box', size:[0.52,0.08,0.01], pos:[0,0.43,0.153], color:0x3a3a3a, metalness:0.6} ] },
  speaker: { th:'ลำโพง',    parts: () => [ {shape:'box', size:[0.4,0.7,0.35], pos:[0,0.35,0], color:0x151515},
                              {shape:'cylinder', size:[0.13,0.13,0.02], pos:[0,0.25,0.18], rot:[90,0,0], color:0x333333}, {shape:'cylinder', size:[0.05,0.05,0.02], pos:[0,0.52,0.18], rot:[90,0,0], color:0x333333} ] },
  mic:     { th:'ไมค์',     parts: () => [ {shape:'cylinder', size:[0.15,0.15,0.02], pos:[0,0.01,0], color:0x777777, metalness:0.8},
                              {shape:'cylinder', size:[0.012,0.012,1.58], pos:[0,0.79,0], color:0x777777, metalness:0.8},
                              {shape:'cylinder', size:[0.01,0.01,0.35], pos:[0,1.58,0.15], rot:[67,0,0], color:0x777777, metalness:0.8},
                              {shape:'capsule', size:[0.03,0.08], pos:[0,1.64,0.3], rot:[67,0,0], color:0x777777, metalness:0.8} ] },
  wall:    { th:'ผนัง',     parts: () => [ {shape:'plane', size:[10,4], pos:[0,2,0], color:0x7a4f3c} ] },
  box:     { th:'กล่อง',    parts: () => [ {shape:'box', size:[0.5,0.5,0.5], pos:[0,0.25,0], color:0x8d8d8d} ] },
  sphere:  { th:'ทรงกลม',   parts: () => [ {shape:'sphere', size:[0.25], pos:[0,0.25,0], color:0x8d8d8d} ] },
  cylinder:{ th:'ทรงกระบอก', parts: () => [ {shape:'cylinder', size:[0.2,0.2,0.6], pos:[0,0.3,0], color:0x8d8d8d} ] },
  guitar:  { th:'กีตาร์',   parts: null }, // built by buildGuitar
  spot:    { th:'สปอตไลท์', parts: null }, // light, handled by the scene
};

export function partGeometry(THREE, p){
  const s = p.size || [];
  switch (p.shape){
    case 'box': return new THREE.BoxGeometry(s[0]||0.5, s[1]||0.5, s[2]||0.5);
    case 'cylinder': return s.length>=3 ? new THREE.CylinderGeometry(s[0], s[1], s[2], 24) : new THREE.CylinderGeometry(s[0]||0.2, s[0]||0.2, s[1]||0.5, 24);
    case 'sphere': return new THREE.SphereGeometry(s[0]||0.25, 24, 16);
    case 'cone': return new THREE.ConeGeometry(s[0]||0.2, s[1]||0.5, 24);
    case 'capsule': return new THREE.CapsuleGeometry(s[0]||0.1, s[1]||0.3, 6, 16);
    case 'plane': return new THREE.PlaneGeometry(s[0]||1, s[1]||1);
    case 'torus': return new THREE.TorusGeometry(s[0]||0.3, s[1]||0.05, 12, 32);
    default: return new THREE.BoxGeometry(0.3,0.3,0.3);
  }
}

export function buildGuitar(THREE, shadow){
  const burst = new THREE.MeshStandardMaterial({color:0xc5752b, roughness:0.4});
  const dark = new THREE.MeshStandardMaterial({color:0x2b1a10, roughness:0.5});
  const metal = new THREE.MeshStandardMaterial({color:0x777777, roughness:0.3, metalness:0.8});
  const g = new THREE.Group(); const s = new THREE.Shape();
  const pts = [[-0.26,0],[-0.25,0.12],[-0.2,0.19],[-0.1,0.2],[-0.04,0.17],[0.0,0.14],[0.05,0.15],[0.12,0.17],[0.18,0.13],[0.2,0.05],[0.2,-0.05],[0.18,-0.13],[0.12,-0.17],[0.05,-0.15],[0.0,-0.14],[-0.04,-0.17],[-0.1,-0.2],[-0.2,-0.19],[-0.25,-0.12]];
  s.moveTo(pts[0][0],pts[0][1]); s.splineThru(pts.slice(1).map(p=>new THREE.Vector2(p[0],p[1]))); s.closePath();
  const body = shadow(new THREE.Mesh(new THREE.ExtrudeGeometry(s,{depth:0.11,bevelEnabled:true,bevelSize:0.01,bevelThickness:0.01}), burst)); body.position.z=-0.055; g.add(body);
  const hole = new THREE.Mesh(new THREE.CircleGeometry(0.045,24), dark); hole.position.set(0.02,0,0.066); g.add(hole);
  const pg = new THREE.Mesh(new THREE.CircleGeometry(0.06,24), dark); pg.scale.set(1,1.3,1); pg.position.set(0.05,-0.07,0.0661); g.add(pg);
  const neck = shadow(new THREE.Mesh(new THREE.BoxGeometry(0.62,0.05,0.03), dark)); neck.position.set(0.45,0,0.04); g.add(neck);
  const hs = shadow(new THREE.Mesh(new THREE.BoxGeometry(0.16,0.07,0.02), dark)); hs.position.set(0.82,0,0.04); g.add(hs);
  const br = new THREE.Mesh(new THREE.BoxGeometry(0.12,0.02,0.01), dark); br.position.set(-0.1,0,0.066); g.add(br);
  for(let i=0;i<6;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(0.95,0.0015,0.0015), metal); st.position.set(0.32,-0.0125+i*0.005,0.072); g.add(st); }
  return g;
}

// Build a THREE.Group for an object spec. shadow(mesh) marks cast/receive. Returns null for non-mesh kinds (spot).
export function buildObject(THREE, obj, shadow = m => m){
  if (obj.kind === 'spot') return null;
  const g = new THREE.Group();
  if (obj.kind === 'guitar') g.add(buildGuitar(THREE, shadow));
  else {
    const lib = LIBRARY[obj.kind];
    const parts = obj.parts || (lib && lib.parts ? lib.parts() : LIBRARY.box.parts());
    for (const p of parts){
      const mat = new THREE.MeshStandardMaterial({ color: (obj.color ?? p.color ?? 0x8d8d8d), roughness: p.roughness ?? 0.8, metalness: p.metalness ?? 0, side: p.shape==='plane' ? THREE.DoubleSide : THREE.FrontSide });
      const m = shadow(new THREE.Mesh(partGeometry(THREE, p), mat));
      m.position.set(...(p.pos || [0,0,0]));
      const r = p.rot || [0,0,0]; m.rotation.order='YXZ'; m.rotation.set(r[0]*Math.PI/180, r[1]*Math.PI/180, r[2]*Math.PI/180);
      g.add(m);
    }
  }
  applyTransform(g, obj);
  return g;
}

export function applyTransform(g, obj){
  g.position.set(...(obj.pos || [0,0,0]));
  const r = obj.rot || [0,0,0]; g.rotation.order = 'YXZ'; g.rotation.set(r[0]*Math.PI/180, r[1]*Math.PI/180, r[2]*Math.PI/180);
  const s = obj.scale ?? 1; if (Array.isArray(s)) g.scale.set(s[0], s[1], s[2]); else g.scale.set(s, s, s);
}

// Convert the legacy harness fields (props stool/mic/wall, guitar) into objects.
export function legacyToObjects(S){
  const out = [];
  if (S.guitar && S.guitar.mode !== 'none') out.push({ id:'guitar', name:'กีตาร์', kind:'guitar', pos:S.guitar.pos, rot:S.guitar.rot, scale:1 });
  for (const p of (S.props || [])){
    if (p.type === 'stool') out.push({ id:'stool', name:'สตูล', kind:'stool', pos:p.pos, rot:[0,0,0], scale: [1, (p.h||0.64)/0.64, 1] });
    if (p.type === 'mic') out.push({ id:'mic', name:'ไมค์', kind:'mic', pos:p.pos, rot:[0,0,0], scale: [1, (p.h||1.58)/1.58, 1] });
    if (p.type === 'spot') out.push({ id:'spot', name:'สปอตไลท์', kind:'spot', pos:p.pos, target:p.target, intensity:p.intensity||40 });
  }
  if (S.wall) out.push({ id:'wall', name:'ผนัง', kind:'wall', pos:[0,0,S.wall.z], rot:[0,0,0], scale:1, color:S.wall.color });
  return out;
}
