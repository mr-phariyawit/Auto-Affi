// Pose specs for the wooden-mannequin draft harness.
// Conventions: figure faces +Z (toward camera). Angles in degrees.
//   arm: fwd (raise forward), out (abduct sideways), bend (elbow), twist
//   leg: fwd (thigh forward), out, bend (knee), foot (toe up)
//   head: headPitch (+ = look down), headYaw (+ = turn to figure's left), headTilt
//   guitar.pos is world [x,y,z]; guitar.rot [x,y,z]; neck points +X (player's left) before rotation.
export const POSES = {
  A: {
    title: 'Americana street, golden hour — full body, guitar on back',
    notes: 'Full body 3:4. Walking past brick wall, guitar slung on back. Warm key from camera-left, low (sunset). Shows jacket, jeans, boots.',
    bg: 0x6b4a3b, wall: {z:-0.9, color:0x7a4f3c}, floor: 0x4b4540,
    cam: {pos:[1.3,1.15,4.3], target:[0,0.92,0], fov:36},
    light: {keyPos:[-4,1.4,3], color:0xffc27a, intensity:2.6, ambient:0.35, rimPos:[3,2,-2], rimColor:0xffe0b0, rimIntensity:0.8},
    guitar: {pos:[0.14,1.08,-0.26], rot:[0,180,55]},
    pose: { bodyYaw: 20, spineLean: 3, headYaw: -15, headPitch: 2,
      armL:{fwd:38, bend:105, out:6}, armR:{fwd:-18, bend:12, out:8},
      legL:{fwd:22, bend:8, foot:8}, legR:{fwd:-14, bend:28, foot:-20} }
  },
  B: {
    title: 'Studio portrait, dark grey seamless — seated on stool',
    notes: '3/4 body 3:4. One large softbox camera-left + soft blue rim. Guitar upright on right thigh, left hand on fretboard, eyes to camera.',
    bg: 0x1d1d1d, floor: 0x1f1f1f,
    cam: {pos:[0.35,1.15,2.7], target:[0,0.95,0.1], fov:38},
    light: {keyPos:[-2.5,2.6,2.4], color:0xfff2e0, intensity:2.4, ambient:0.18, rimPos:[2.2,2.4,-2.2], rimColor:0x9fc0ff, rimIntensity:1.4},
    props: [{type:'stool', pos:[0,0,-0.02], h:0.64}],
    guitar: {pos:[-0.02,0.86,0.36], rot:[-8,-10,32]},
    pose: { rootPos:[0,0.72,0.02], bodyYaw:-8, spineLean:4, headYaw:8, headPitch:4,
      armL:{fwd:30, out:58, bend:70}, armR:{fwd:30, out:12, bend:48, twist:55},
      legL:{fwd:82, bend:92, out:10, foot:0}, legR:{fwd:85, bend:88, out:14, foot:0} }
  },
  F: {
    title: 'Live stage, small club — spotlight + haze',
    notes: 'Mid-song at vintage mic, top-front spotlight, dark audience side. Low camera from the crowd. Guitar strapped at waist. Likeness risk: eyes closed / angle — round 2.',
    bg: 0x060606, floor: 0x0d0d0d,
    cam: {pos:[-0.9,1.0,3.1], target:[0,1.25,0.05], fov:40},
    light: {keyPos:[0.6,4,2.2], color:0xfff4d6, intensity:0.6, ambient:0.08, rimPos:[-2.5,2.5,-2.5], rimColor:0xff5c3a, rimIntensity:1.6},
    props: [{type:'mic', pos:[0.02,0,0.42], h:1.58}, {type:'spot', pos:[0.5,4.2,2.0], target:[0,1.2,0], intensity:60}],
    guitar: {pos:[0.06,0.96,0.24], rot:[-10,0,22]},
    pose: { bodyYaw:-5, spineLean:6, headPitch:-6, headYaw:3, headTilt:-4,
      armL:{fwd:26, out:52, bend:72}, armR:{fwd:28, out:10, bend:50, twist:55},
      legL:{out:9, fwd:4}, legR:{out:9, fwd:-4, bend:4} }
  },
  G: {
    title: 'Close-up editorial, high-key light grey',
    notes: 'Chest-up 3:4. Guitar neck crosses the frame diagonally from bottom-right, fretting hand high, gaze slightly off-camera. Big soft key camera-left, one catchlight. Profile/avatar use.',
    bg: 0xd9d9d9, floor: 0xcfcfcf,
    cam: {pos:[0.3,1.6,2.0], target:[0,1.45,0.1], fov:34},
    light: {keyPos:[-2,3,2.2], color:0xffffff, intensity:2.0, ambient:0.95, rimPos:[2,2.5,-1.5], rimColor:0xffffff, rimIntensity:0.6},
    guitar: {pos:[-0.02,1.0,0.34], rot:[-12,-6,68]},
    pose: { bodyYaw:-6, spineLean:3, headYaw:16, headTilt:5, headPitch:3,
      armL:{fwd:62, out:22, bend:110}, armR:{fwd:34, out:8, bend:55, twist:60},
      legL:{}, legR:{} }
  }
};
