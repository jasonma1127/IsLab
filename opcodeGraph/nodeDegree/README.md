# Experiment Results

![image](https://user-images.githubusercontent.com/33441316/177007611-7b2f259c-4622-4209-a6f8-a24bcdaf7cd0.png)

![image](https://user-images.githubusercontent.com/33441316/177007886-4abecde6-fa89-4944-abd8-d5496edacbde.png)

以下為 76211 (M : 43298, B : 32913) 筆數為例 : 

### With REs

- COG_time: 01:57:13
- REs_time: 01:02:20
- CND_time: 00:00:27
- total_time: 03:00:01
- Feature extraction per file time: 0.1417356151425842

### Without REs

- COG_time: 01:50:38
- CND_time: 00:00:40
- total_time: 02:07:13
- Feature extraction per file time: 0.10015881176522695

### 小結

- 本次實驗解決了 memory 不斷疊加的問題。
- 發現存取 opcode graph 花費的時間遠大於建立的時間，所以索性不存圖了，直接轉成可訓練的 feature。

# Dataset

- CPU arch : armel
- Malware : 1000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 1000

feature shape : 987

## with Remove Edges ##

- xData shape : (2000, 987)
- yLabel shape : (2000,)

- X_train shape : (1600, 987)
- y_train shape : (1600,)

- X_test shape : (400, 987)
- y_test shape : (400,)

Training time: 0.3736226558685303 s

Predicting time: 0.012392044067382812 s

> Accuracy : 1.0

## without Remove Edges ##

- xData shape : (2000, 987)
- yLabel shape : (2000,)

- X_train shape : (1600, 987)
- y_train shape : (1600,)

- X_test shape : (400, 987)
- y_test shape : (400,)

Training time: 0.2985117435455322 s

Predicting time: 0.012912511825561523 s

> Accuracy : 1.0

---

# Dataset

- CPU arch : armel
- Malware : 5000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 5000

feature shape : 1346

## With Remove Edges

- xData shape : (10000, 1346)
- yLabel shape : (10000,)

- X_train shape : (8000, 1346)
- y_train shape : (8000,)

- X_test shape : (2000, 1346)
- y_test shape : (2000,)

Training time: 1.1084108352661133 s

Predicting time: 0.029042720794677734 s

> Accuracy : 1.0

## Without Remove Edges

- xData shape : (10000, 1346)
- yLabel shape : (10000,)

- X_train shape : (8000, 1346)
- y_train shape : (8000,)

- X_test shape : (2000, 1346)
- y_test shape : (2000,)

Training time: 1.4482789039611816 s

Predicting time: 0.027620553970336914 s

> Accuracy : 1.0

---

# Dataset

- CPU arch : armel
- Malware : 10000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 10000

feature shape : 1483

## With Remove Edges

- xData shape : (20000, 1483)
- yLabel shape : (20000,)

- X_train shape : (16000, 1483)
- y_train shape : (16000,)

- X_test shape : (4000, 1483)
- y_test shape : (4000,)

Training time: 2.5792829990386963 s

Predicting time: 0.12560009956359863 s

> Accuracy : 1.0

## Without Remove Edges

- xData shape : (20000, 1483)
- yLabel shape : (20000,)

- X_train shape : (16000, 1483)
- y_train shape : (16000,)

- X_test shape : (4000, 1483)
- y_test shape : (4000,)

Training time: 2.2786951065063477 s

Predicting time: 0.0482635498046875 s

> Accuracy : 1.0

---

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

---

![image](https://user-images.githubusercontent.com/33441316/177270252-d8cc771b-5240-40ca-9678-a27cc28e35dd.png)

以上是四種不同的資料集數量對準確率的影響，也許都是在相同的 CPU 架構下，所以準確率都會維持在一個相當高的水準，並不會因為 malware family 變得複雜後而下降。

並且在 With REs 與 Without REs 分別測試下，準確率都維持在 1，也就可以證明說，With REs 並不會對準確率產生影響。

![image](https://user-images.githubusercontent.com/33441316/177001604-1c4a0e3a-0a15-4a8f-939d-6ca67b22a6fb.png)

以上有四種不同的資料集數量對維度的影喜，隨著資料集的擴增，訓練的維度也不斷上升，而隨著維度的不斷加大，預計訓練的時間也會有些許影響。

![image](https://user-images.githubusercontent.com/33441316/177316531-e6de8145-b79f-4141-968c-242f4c8216ad.png)

上圖有針對 With REs 與 Without REs 做一個時間上的比較，原本想說因為 Without REs 的話，就會有許多雜訊，訓練起來的資料量比較多，應該所花費的時間就會比較多，但上圖中並沒有發現這樣的跡象，所以 REs 這個過程並不會在 training 這邊省去時間。

![image](https://user-images.githubusercontent.com/33441316/177004344-77cac05c-dcff-40e5-8afd-1a1b94dfcead.png)

上圖是針對 With REs 與 Without REs 的 predicting time 做一個時間上的調查。發現也沒有太大的區別。

綜合以上的實驗總結出以下幾點 : 

- With or Without REs 對於 Accuracy, training time 與 predicting time 幾乎沒有影響。
- REs 並無消除雜訊，提高 Accuracy 之作用。
- REs 在降低資訊量的同時，也沒有對 training 與 predicting 的時間縮減，甚至增加了建立 feature 的時間。


目前只有在單一 CPU 架構跑此實驗，計畫要跑多重架構下的情境，會不會遇到 Accuracy 下降的問題，或是維度問題，因為 opcode graph 的跨架構是目前廣為人知的挑戰之一。


