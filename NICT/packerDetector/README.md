# Packer Detector

## How To Use?

`python3 packerDetector.py /data/total_entropy_with_section.json`

If it works properly, you can see the result below.

```
[+] Reading Data...
[+] Creating Feature...
[+] Creating Label...
[+] Extracting label...: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1572317/1572317 [00:00<00:00, 1589173.75it/s]
                                                        mean       max       min  label
0000002158d35c2bb5e7d96a39ff464ea4c83de8c5fd720...  3.314734  6.324158  0.000000      0
0000002a10959ec38b808d8252eed2e814294fbb25d2cd0...  3.406368  6.569293  0.000000      0
00000391058cf784a3e1a3f4babfb2e02b74857178cfdc3...  6.035743  7.938660  2.229959      1
00000ef0e4f972c11260234c9e8308ef67883828a39d42d...  6.035745  7.938660  2.229959      1
0000174b098ffbbab221cd21cc7d7c4217abbc923e223f8...  3.288118  5.775641  0.000000      0
...                                                      ...       ...       ...    ...
ffffc0f59240fea340c397e6af364680ef0563084a69151...  3.382601  6.317504  0.000000      0
ffffc78c18dea9e2b6a355df336c1264c11e9fc909d614a...  3.827518  5.635785  1.000000      0
ffffd21da8f974c48a37e5528ed806b021d87a0dad84987...  3.379810  6.317480  0.000000      0
ffffdbb415e01c0d5b49182ee54f7ed3e9259c01c09115c...  3.426462  6.313573  0.000000      0
ffffe5e69a4c3034403b22772eeabb239b5f60e5ad9e1eb...  3.426499  6.313573  0.000000      0

[1572317 rows x 4 columns]

Training shape: 1053452
Testing shape: 518865

Accuracy: 0.9907952935734728
```
