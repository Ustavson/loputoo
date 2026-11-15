# Data manifest

Raw data is not in git. This file is the record of what exists and where it is
backed up. One row per capture session.

| ID | Date | Location | Device / lens | Mode & settings | Frames / length | Path in `data/` | Backup location | Notes |
|----|------|----------|---------------|-----------------|-----------------|-----------------|-----------------|-------|
| 20261103_test_1 | 2026-11-03 | ? (fill in) | iPhone 16, main lens | Video 1080p30, HLG HDR, portrait | 5 videos: long_2_way 472 s, short_1_way 38 s, short_2_way 64 s, hole2 414 s, hole1 415 s | `videos/2026-11-03/` | none yet | Filmed 15:29-15:52 local time. Overcast. First test videos: motion blur and fast pans broke COLMAP on hole1/hole2 (see LOG 2026-11-03) |
| 20261114_tartu_1 | 2026-11-14 | ? (fill in): suur, roosi_jaama, ujula, sild | iPhone 16, main lens | Video 1080p30, HLG HDR, portrait | suur_part1 142 s + suur_part2 396 s, roosi_jaama 230 s, ujula 271 s, sild 273 s | `videos/2026-11-14/` | none yet | Filmed 14:09-14:54 local time. `suur.MOV` = part1 + part2 joined back to back with ffmpeg (stream copy, no re-encode, 538 s); part2 starts where part1 ended (a crosswalk, ~46 s pause) |

**ID** convention: `YYYYMMDD_<place>_<n>`, e.g. `20261108_raekoja-plats_1`.
Record weather and time of day in Notes: lighting consistency matters a lot for splats.
