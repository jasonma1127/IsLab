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
