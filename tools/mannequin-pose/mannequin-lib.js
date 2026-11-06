// Shared jointed wooden mannequin (used by the headless harness and the poser page).
// buildMannequin(THREE, shadowFn) -> { root, J:{name:{g,kind,side,ball,foot?}}, pickables:[meshes with userData.joint], anchors:{handL,handR} (groups at the palms; parent objects here with attach:{fig,anchor}) }
// applyPoseTo(mq, pose) sets joint rotations from the semantic pose object (see skills/mannequin-poser/references/scene-schema.md).
const D = Math.PI/180;

export function buildMannequin(THREE, sh = m => m, opts = {}){
  const wood = new THREE.MeshStandardMaterial({color: opts.woodColor ?? 0xc9a06a, roughness:0.75});
  const jointM = new THREE.MeshStandardMaterial({color: opts.jointColor ?? 0x8c6a3f, roughness:0.6});
  const dark = new THREE.MeshStandardMaterial({color:0x2b1a10, roughness:0.5});
  const J = {}, pickables = [], anchors = {};
  const mkJoint = (name, kind, side, r) => { const g = new THREE.Group(); const b = sh(new THREE.Mesh(new THREE.SphereGeometry(r,20,14), jointM)); b.userData.joint = name; g.add(b); pickables.push(b); J[name] = {g, kind, side, ball:b}; return g; };
  const limbMesh = (len, r, name) => { const m = sh(new THREE.Mesh(new THREE.CapsuleGeometry(r, Math.max(len-2*r,0.01), 6, 16), wood)); m.position.y = -len/2; m.userData.joint = name; pickables.push(m); return m; };
  const blob = (sx,sy,sz,y,name) => { const m = sh(new THREE.Mesh(new THREE.SphereGeometry(1,24,16), wood)); m.scale.set(sx,sy,sz); m.position.y=y; m.userData.joint=name; pickables.push(m); return m; };

  const root = new THREE.Group();
  root.add(blob(0.17,0.11,0.12,0,'spine'));
  const spine = mkJoint('spine','spine',0,0.05); spine.position.y = 0.08; root.add(spine);
  spine.add(blob(0.15,0.11,0.11,0.11,'spine'));
  const chest = mkJoint('chest','spine',0,0.05); chest.position.y = 0.22; spine.add(chest);
  chest.add(blob(0.19,0.15,0.13,0.15,'chest'));
  const neckG = new THREE.Group(); neckG.position.y = 0.30; chest.add(neckG);
  const neckM = sh(new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.05,0.09,16), wood)); neckM.position.y=0.045; neckG.add(neckM);
  const head = mkJoint('head','head',0,0.03); head.position.y = 0.09; neckG.add(head);
  head.add(blob(0.095,0.12,0.105,0.12,'head'));
  const nose = sh(new THREE.Mesh(new THREE.ConeGeometry(0.018,0.04,12), jointM)); nose.rotation.x=Math.PI/2; nose.position.set(0,0.11,0.105); head.add(nose);
  for (const sx of [-0.035,0.035]){ const e = new THREE.Mesh(new THREE.SphereGeometry(0.012,10,8), dark); e.position.set(sx,0.14,0.095); head.add(e); }
  for (const [side,L] of [[1,'L'],[-1,'R']]){
    const sh0 = new THREE.Group(); sh0.position.set(side*0.21, 0.27, 0); chest.add(sh0);
    const up = mkJoint('arm'+L,'arm',side,0.05); up.add(limbMesh(0.30,0.045,'arm'+L)); sh0.add(up);
    const fo = mkJoint('fore'+L,'fore',side,0.045); fo.position.y=-0.30; fo.add(limbMesh(0.27,0.04,'fore'+L)); up.add(fo);
    const hand = sh(new THREE.Mesh(new THREE.SphereGeometry(1,16,12), jointM)); hand.scale.set(0.04,0.07,0.025); hand.position.y=-0.33; hand.userData.joint='fore'+L; pickables.push(hand); fo.add(hand);
    const anchor = new THREE.Group(); anchor.position.y = -0.35; anchor.name = 'hand'+L; fo.add(anchor); anchors['hand'+L] = anchor;
    const hip = new THREE.Group(); hip.position.set(side*0.10,-0.05,0); root.add(hip);
    const th = mkJoint('leg'+L,'leg',side,0.07); th.add(limbMesh(0.43,0.065,'leg'+L)); hip.add(th);
    const sn = mkJoint('shin'+L,'shin',side,0.055); sn.position.y=-0.43; sn.add(limbMesh(0.42,0.05,'shin'+L)); th.add(sn);
    const ft = sh(new THREE.Mesh(new THREE.BoxGeometry(0.08,0.05,0.25), jointM)); ft.position.set(0,-0.445,0.08); ft.userData.joint='shin'+L; pickables.push(ft); sn.add(ft); J['shin'+L].foot = ft;
  }
  return { root, J, pickables, anchors, mats:{wood, jointM} };
}

const setRot = (o,x,y,z,order) => { o.rotation.order = order; o.rotation.set(x*D,y*D,z*D); };

export function applyPoseTo(mq, p){
  const { root, J } = mq;
  root.position.set(...(p.rootPos||[0,0.98,0])); setRot(root,0,p.bodyYaw||0,0,'YXZ');
  setRot(J.spine.g, p.spineLean||0, p.spineTwist||0, p.spineTilt||0, 'YXZ');
  setRot(J.chest.g, p.chestLean||0, p.chestTwist||0, 0, 'YXZ');
  setRot(J.head.g, p.headPitch||0, p.headYaw||0, p.headTilt||0, 'YXZ');
  for (const [L,side] of [['L',1],['R',-1]]){
    const a = p['arm'+L]||{}, l = p['leg'+L]||{};
    setRot(J['arm'+L].g, -(a.fwd||0), a.twist||0, side*(a.out||0), 'ZXY');
    setRot(J['fore'+L].g, -(a.bend||0), a.foreTwist||0, 0, 'YXZ');
    setRot(J['leg'+L].g, -(l.fwd||0), l.twist||0, side*(l.out||0), 'ZXY');
    setRot(J['shin'+L].g, l.bend||0, 0, 0, 'YXZ');
    J['shin'+L].foot.rotation.x = -(l.foot||0)*D;
  }
}

// After a gizmo drag on joint `name`: write the euler back into the semantic pose object.
export function readBackJoint(mq, name, p){
  const j = mq.J[name], r = j.g.rotation, L = name.slice(-1), side = j.side, R = v=>Math.round(v/D);
  if (j.kind==='arm'){ const a = p['arm'+L] = p['arm'+L]||{}; a.fwd = -R(r.x); a.twist = R(r.y); a.out = side*R(r.z); }
  else if (j.kind==='fore'){ const a = p['arm'+L] = p['arm'+L]||{}; a.bend = -R(r.x); a.foreTwist = R(r.y); }
  else if (j.kind==='leg'){ const l = p['leg'+L] = p['leg'+L]||{}; l.fwd = -R(r.x); l.twist = R(r.y); l.out = side*R(r.z); }
  else if (j.kind==='shin'){ const l = p['leg'+L] = p['leg'+L]||{}; l.bend = R(r.x); }
  else if (name==='head'){ p.headPitch=R(r.x); p.headYaw=R(r.y); p.headTilt=R(r.z); }
  else if (name==='spine'){ p.spineLean=R(r.x); p.spineTwist=R(r.y); p.spineTilt=R(r.z); }
  else if (name==='chest'){ p.chestLean=R(r.x); p.chestTwist=R(r.y); }
}
