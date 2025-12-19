# ⚡ Crypto Arbitrage Scanner (Kripto Para Arbitraj Tarayıcısı)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Finance](https://img.shields.io/badge/Domain-FinTech-green)

Bu proje, **Finans Dersi Dönem Sonu Projesi** kapsamında geliştirilmiş, merkezi kripto para borsaları (CEX) arasındaki fiyat verimsizliklerini (price inefficiencies) analiz ederek arbitraj fırsatlarını tespit eden gerçek zamanlı bir finansal analiz aracıdır.

[Canlı Demo Linki Buraya Gelecek] (Opsiyonel)

---

## 🎯 Projenin Amacı ve Finansal Teori

Bu proje, finans literatüründeki **Tek Fiyat Kanunu (Law of One Price)** ilkesine dayanır. Teorik olarak etkin bir piyasada, aynı varlığın (örneğin Bitcoin) tüm piyasalarda aynı fiyata sahip olması gerekir.

Ancak gerçek dünyada:
* Likidite farkları,
* Bölgesel talep dengesizlikleri,
* Veri transferindeki gecikmeler

nedeniyle borsalar arasında **Fiyat Farkları (Spread)** oluşur. Bu yazılım, bu farkları yakalayarak yatırımcıya **Risksiz Getiri (Risk-Free Profit)** imkanı sunan arbitraj fırsatlarını, **işlem maliyetlerini (komisyonları)** de hesaba katarak simüle eder.

---

## 🚀 Özellikler

* **Çoklu Borsa Taraması:** Binance, Kraken, Coinbase ve KuCoin gibi majör borsalardan eş zamanlı fiyat çekimi.
* **Gerçek Zamanlı Veri:** `CCXT` kütüphanesi kullanılarak API üzerinden anlık veri akışı.
* **Net Kar Simülasyonu:** Sadece fiyat farkını değil, borsa komisyon oranlarını (Trading Fees) da hesaba katarak gerçekçi kar/zarar hesabı.
* **Görselleştirme:** Fiyat dağılımlarının karşılaştırmalı grafik analizi.
* **Kullanıcı Dostu Arayüz:** Streamlit tabanlı modern web arayüzü.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda (Localhost) çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
* Python 3.8 veya üzeri
* İnternet bağlantısı (API verileri için)

### Adım 1: Projeyi Kopyalayın
```bash
git clone [https://github.com/KULLANICI_ADINIZ/repo-isminiz.git](https://github.com/KULLANICI_ADINIZ/repo-isminiz.git)
cd repo-isminiz
Adım 2: Sanal Ortamı Kurun (Önerilen)
Bash

# Windows için
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux için
python3 -m venv venv
source venv/bin/activate
Adım 3: Kütüphaneleri Yükleyin
Bash

pip install -r requirements.txt
Adım 4: Uygulamayı Başlatın
Bash

streamlit run arbitraj.py
📂 Proje Yapısı
├── arbitraj.py          # Ana uygulama kodu (Backend + Frontend)
├── requirements.txt     # Gerekli Python kütüphaneleri
└── README.md            # Proje dokümantasyonu
🧮 Kullanılan Teknolojiler
Python: Ana programlama dili.

Streamlit: Web arayüzü ve dashboard oluşturma.

CCXT (CryptoCurrency eXchange Trading Library): 100+ borsadan veri çekmek için kullanılan standart kütüphane.

Pandas: Veri manipülasyonu ve tablolama.

⚠️ Yasal Uyarı
Bu proje eğitim amaçlı geliştirilmiştir. Gösterilen veriler anlık piyasa koşullarına göre değişebilir ve yatırım tavsiyesi niteliği taşımaz.

Geliştirici: Ozan Efe Özdemir
