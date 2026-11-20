#!/bin/bash
# EP05 mix (adapted from EP04): 13 VO takes at timing.json vo_start, EP01 Suno music (42.7 s, looped x4 via stream_loop 3) ducked under VO by sidechain, sparse synth SFX.
# Run from output/thai-cooking-channel. Generated from audio/timing.json.
set -e
E=ep05-kaeng-khiao-wan/audio; S=ep01-pad-kra-pao/audio/sfx/synth; M=ep01-pad-kra-pao/audio/music/suno_v1.mp3; END=156.14
V=$E/vo-en-v1
# SFX: plate@0.15, mortar@66.45, pour@104.25, sizzle@105.2, sizzle@116.1, leaves@124.2, leaves@139.4, plate@153.3
ffmpeg -y -v error \
 -i $V/line_01.wav -i $V/line_02.wav -i $V/line_03.wav -i $V/line_04.wav -i $V/line_05.wav -i $V/line_06.wav -i $V/line_07.wav -i $V/line_08.wav -i $V/line_09.wav -i $V/line_10.wav -i $V/line_11.wav -i $V/line_12a.wav -i $V/line_12b.wav \
 -stream_loop 3 -i $M -i $S/plate.wav -i $S/mortar.wav -i $S/pour.wav -i $S/sizzle.wav -i $S/sizzle.wav -i $S/leaves.wav -i $S/leaves.wav -i $S/plate.wav \
 -filter_complex "\
[0:a]adelay=350:all=1[v0];[1:a]adelay=14980:all=1[v1];[2:a]adelay=28610:all=1[v2];[3:a]adelay=43920:all=1[v3];[4:a]adelay=53550:all=1[v4];[5:a]adelay=66700:all=1[v5];[6:a]adelay=77610:all=1[v6];[7:a]adelay=90920:all=1[v7];[8:a]adelay=104430:all=1[v8];[9:a]adelay=116300:all=1[v9];[10:a]adelay=128690:all=1[v10];[11:a]adelay=139600:all=1[v11];[12:a]adelay=152620:all=1[v12];\
[v0][v1][v2][v3][v4][v5][v6][v7][v8][v9][v10][v11][v12]amix=inputs=13:normalize=0,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$END,atrim=0:$END,asplit=2[vo][sc];\
[13:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:$END,afade=t=out:st=154.34:d=1.8,volume=0.32[mu];\
[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mud];\
[14:a]adelay=150:all=1,volume=0.5[s0];[15:a]adelay=66450:all=1,volume=0.45[s1];[16:a]adelay=104250:all=1,volume=0.4[s2];[17:a]adelay=105200:all=1,volume=0.35[s3];[18:a]adelay=116100:all=1,volume=0.3[s4];[19:a]adelay=124200:all=1,volume=0.45[s5];[20:a]adelay=139400:all=1,volume=0.45[s6];[21:a]adelay=153300:all=1,volume=0.5[s7];\
[s0][s1][s2][s3][s4][s5][s6][s7]amix=inputs=8:normalize=0,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$END,atrim=0:$END[sfx];\
[vo][mud][sfx]amix=inputs=3:normalize=0,atrim=0:$END[pre]" -map "[pre]" -c:a pcm_s16le $E/mix-pre.wav
# two-pass loudnorm to -14 LUFS, TP -2.5 (AAC encode pushes peaks up ~0.6 dB)
J=$(ffmpeg -v info -i $E/mix-pre.wav -af loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -v error -i $E/mix-pre.wav -af "loudnorm=I=-14:TP=-2.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s16le $E/mix.wav
