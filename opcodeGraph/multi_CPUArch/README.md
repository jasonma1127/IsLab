# Dataset

- CPU arch : armel, mipseb, x86el, mipsel, x86_64el, unknown, ppceb, sparceb, mips64eb, armeb, ppcel, m68keb
- Malware : 1000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 1000

feature shape : 1583

## With Remove Edges

xData shape : (2000, 1583)
yLabel shape : (2000,)

X_train shape : (1600, 1583)
y_train shape : (1600,)

X_test shape : (400, 1583)
y_test shape : (400,)

Training time: 1.0544123649597168 s

Predicting time: 0.24966979026794434 s

Accuracy : 1.0

## Without Remove Edges

xData shape : (2000, 1583)
yLabel shape : (2000,)

X_train shape : (1600, 1583)
y_train shape : (1600,)

X_test shape : (400, 1583)
y_test shape : (400,)

Training time: 1.3162615299224854 s

Predicting time: 0.2603583335876465 s

Accuracy : 1.0

---

# Dataset

- CPU arch : armel, mipseb, x86el, mipsel, x86_64el, unknown, ppceb, sparceb, mips64eb, armeb, ppcel, m68keb
- Malware : 5000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 5000

feature shape : 1930

## With Remove Edges

xData shape : (10000, 1930)
yLabel shape : (10000,)

X_train shape : (8000, 1930)
y_train shape : (8000,)

X_test shape : (2000, 1930)
y_test shape : (2000,)

Training time: 5.026396751403809 s

Predicting time: 1.4458441734313965 s

Accuracy : 1.0

## Without Remove Edges

xData shape : (10000, 1930)
yLabel shape : (10000,)

X_train shape : (8000, 1930)
y_train shape : (8000,)

X_test shape : (2000, 1930)
y_test shape : (2000,)

Training time: 7.228598594665527 s

Predicting time: 1.5377748012542725 s

Accuracy : 1.0

---

# Dataset

- CPU arch : armel, mipseb, x86el, mipsel, x86_64el, unknown, ppceb, sparceb, mips64eb, armeb, ppcel, m68keb
- Malware : 10000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 10000

feature shape : 2262

## With Remove Edges

xData shape : (20000, 2262)
yLabel shape : (20000,)

X_train shape : (16000, 2262)
y_train shape : (16000,)

X_test shape : (4000, 2262)
y_test shape : (4000,)

Training time: 13.908692836761475 s

Predicting time: 2.929856061935425 s

Accuracy : 1.0

## Without Remove Edges

xData shape : (20000, 2262)
yLabel shape : (20000,)

X_train shape : (16000, 2262)
y_train shape : (16000,)

X_test shape : (4000, 2262)
y_test shape : (4000,)

Training time: 15.849522113800049 s

Predicting time: 3.3586983680725098 s

Accuracy : 1.0


# Dataset

- CPU arch : armel, mipseb, x86el, mipsel, x86_64el, unknown, ppceb, sparceb, mips64eb, armeb, ppcel, m68keb
- Malware : 50000 (Mirai, Bashlite, unknown, Android, Tsunami, Dofloo, Hajime, Xorddos, Pnscan)
- Benign : 50000

feature shape : 3211

## With Remove Edges

xData shape : (100000, 3211)
yLabel shape : (100000,)

X_train shape : (80000, 3211)
y_train shape : (80000,)

X_test shape : (20000, 3211)
y_test shape : (20000,)

Training time: 104.3819899559021 s

Predicting time: 23.867090702056885 s

Accuracy : 1.0

## Without Remove Edges

xData shape : (100000, 3211)
yLabel shape : (100000,)

X_train shape : (80000, 3211)
y_train shape : (80000,)

X_test shape : (20000, 3211)
y_test shape : (20000,)

Training time: 98.32340049743652 s

Predicting time: 25.383112907409668 s

Accuracy : 1.0

--- 

![image](https://user-images.githubusercontent.com/33441316/180685129-e20e5a9c-19ee-4c10-a9d3-5ab0c9ed204c.png)

CPU 架構變得複雜，Malware 家族也變得複雜，但準確率依然維持 100%。

![image](https://user-images.githubusercontent.com/33441316/180685209-ae527e22-d4db-491f-a71b-200801da2412.png)

上圖是單一 CPU 架構與多重 CPU 架構在相同數量的資料集的維度對比，可以明顯看出兩著維度的差異。

![image](https://user-images.githubusercontent.com/33441316/180686627-87b7e247-52d8-4855-80d0-01c09e5ae087.png)

利用 T-SNE 來驗證，明顯看出 malware 與 benign 確實存在很大的差異，所以 detection 比較好分。

![image](https://user-images.githubusercontent.com/33441316/180692029-73233d5f-ec04-4949-bc3e-d34f810e4af8.png)

在 training 中，單一 CPU 架構與多重 CPU 架構在時間上的比較蠻明顯的。

![image](https://user-images.githubusercontent.com/33441316/180692117-7b8c6051-6ce5-4cbe-a095-c7b774e8fcea.png)

在 testing 中，單一 CPU 架構與多重 CPU 架構在時間上的比較就看不出太大的差別。

# 結論

看起來同時在 multiple family 與 multiple CPUArch 的情況下，此方法的 detection accuracy rate 的表現都是非常好的!

- 所以在目前的 dataset 中，With REs 與 Without REs 是沒有差異的，因為此篇的方法是實作在 PE 的資料集上，所以可能存在 dataset 本身的複雜性的不同。
- 因為此 dataset 中的 malware 都是 botnet 類型的，所以推測在 opcode 的數量上面就有很大的差異，
