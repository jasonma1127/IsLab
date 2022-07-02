# Experiment Results

# Dataset

- CPU arch : armel
- Malware : 43298 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 32913

feature shape : 2005

## With Remove Edges

- xData shape : (76211, 2005)
- yLabel shape : (76211,)

- X_train shape : (60968, 2005)
- y_train shape : (60968,)

- X_test shape : (15243, 2005)
- y_test shape : (15243,)

Training time: 8.408792495727539 s

Predicting time: 0.20657944679260254 s

> Accuracy : 1.0

## Without Remove Edges

- xData shape : (76211, 2005)
- yLabel shape : (76211,)

- X_train shape : (60968, 2005)
- y_train shape : (60968,)

- X_test shape : (15243, 2005)
- y_test shape : (15243,)

Training time: 8.21454930305481 s

Predicting time: 0.1782376766204834 s

> Accuracy : 1.0




