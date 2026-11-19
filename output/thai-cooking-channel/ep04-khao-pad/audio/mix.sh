#!/bin/bash
# EP04 mix: VO at timing.json vo_start, EP01 Suno music (looped once, it is 42.7 s) ducked under VO, synth SFX. Run from output/thai-cooking-channel.
set -e
E=ep04-khao-pad/audio; S=ep01-pad-kra-pao/audio/sfx/synth; M=ep01-pad-kra-pao/audio/music/suno_v1.mp3; END=44.81
V=$E/vo-en-v1
ffmpeg -y -v error \
 -i $V/line_01.wav -i $V/line_02.wav -i $V/line_03.wav -i $V/line_04.wav -i $V/line_05.wav -i $V/line_06.wav -i $V/line_07.wav -i $V/line_08.wav \
 -stream_loop 1 -i $M -i $S/plate.wav -i $S/sizzle.wav -i $S/sizzle.wav -i $S/pour.wav -i $S/pepper.wav -i $S/leaves.wav -i $S/plate.wav \
 -filter_complex "\
[0:a]adelay=350:all=1[v0];[1:a]adelay=6020:all=1[v1];[2:a]adelay=10490:all=1[v2];[3:a]adelay=15840:all=1[v3];\
[4:a]adelay=20190:all=1[v4];[5:a]adelay=25070:all=1[v5];[6:a]adelay=30020:all=1[v6];[7:a]adelay=36770:all=1[v7];\
[v0][v1][v2][v3][v4][v5][v6][v7]amix=inputs=8:normalize=0,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$END,atrim=0:$END,asplit=2[vo][sc];\
[8:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:$END,afade=t=out:st=43.02:d=1.79,volume=0.32[mu];\
[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mud];\
[9:a]adelay=150:all=1,volume=0.5[s1];[10:a]adelay=10300:all=1,volume=0.35[s2];\
[11:a]adelay=15600:all=1,volume=0.35[s3];[12:a]adelay=19950:all=1,volume=0.4[s4];\
[13:a]adelay=24850:all=1,volume=0.5[s5];[14:a]adelay=29850:all=1,volume=0.5[s6];[15:a]adelay=36550:all=1,volume=0.5[s7];\
[s1][s2][s3][s4][s5][s6][s7]amix=inputs=7:normalize=0,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$END,atrim=0:$END[sfx];\
[vo][mud][sfx]amix=inputs=3:normalize=0,atrim=0:$END[pre]" -map "[pre]" -c:a pcm_s16le $E/mix-pre.wav
# two-pass loudnorm to -14 LUFS, TP -2 (AAC encode adds ~0.4 dB; EP04 v1 hit -0.8 with -1.5)
J=$(ffmpeg -v info -i $E/mix-pre.wav -af loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -v error -i $E/mix-pre.wav -af "loudnorm=I=-14:TP=-2.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s16le $E/mix.wav
