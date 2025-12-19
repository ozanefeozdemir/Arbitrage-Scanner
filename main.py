import streamlit as st
import ccxt
import pandas as pd
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Crypto Arbitraj Tarayıcısı", layout="wide")

st.title("⚡ Kripto Para Arbitraj Tarayıcısı")
st.markdown("""
Bu uygulama, farklı kripto para borsalarındaki fiyat farklarını (spread) analiz ederek 
**arbitraj** (risksiz kar) fırsatlarını tespit eder.
""")

# --- YAN MENÜ ---
st.sidebar.header("Ayarlar")
secilen_coin = st.sidebar.selectbox("Coin Seçin", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT"])
yatirim_miktari = st.sidebar.number_input("Yatırım Miktarı ($)", min_value=100, value=1000)
komisyon_orani = st.sidebar.slider("Tahmini Borsa Komisyonu (%)", 0.0, 1.0, 0.2) / 100

# --- FONKSİYONLAR ---
# CCXT ile borsalardan fiyat çekme fonksiyonu
def fiyatlari_getir(symbol):
    # Kullanacağımız borsalar (Halka açık verileri kullanacağız)
    borsalar = [ccxt.binance(), ccxt.kraken(), ccxt.coinbase(), ccxt.kucoin()]
    veri_listesi = []

    my_bar = st.progress(0)
    step = 100 / len(borsalar)
    
    for i, borsa in enumerate(borsalar):
        try:
            # Kraken ve Coinbase bazen USDT yerine USD kullanır, basit bir dönüşüm mantığı
            arama_sembolu = symbol
            if borsa.id in ['kraken', 'coinbase'] and symbol.endswith('USDT'):
                arama_sembolu = symbol.replace('USDT', 'USD')
            
            ticker = borsa.fetch_ticker(arama_sembolu)
            fiyat = ticker['last'] # Son işlem fiyatı
            
            veri_listesi.append({
                "Borsa": borsa.name,
                "Fiyat ($)": float(fiyat),
                "Sembol": arama_sembolu
            })
        except Exception as e:
            # Hata verirse (bazı borsalarda o coin olmayabilir) pas geç
            pass
        finally:
            my_bar.progress(int((i + 1) * step))
            
    my_bar.empty() # Yükleme çubuğunu temizle
    return pd.DataFrame(veri_listesi)

# --- ANA AKIŞ ---

if st.button("Fiyatları Tara ve Analiz Et"):
    with st.spinner(f'{secilen_coin} için borsalar taranıyor...'):
        df = fiyatlari_getir(secilen_coin)
    
    if not df.empty:
        # En ucuz ve En pahalıyı bulma
        en_ucuz = df.loc[df['Fiyat ($)'].idxmin()]
        en_pahali = df.loc[df['Fiyat ($)'].idxmax()]
        
        min_fiyat = en_ucuz['Fiyat ($)']
        max_fiyat = en_pahali['Fiyat ($)']
        
        # Arbitraj Hesaplamaları
        fiyat_farki = max_fiyat - min_fiyat
        yuzdesel_fark = (fiyat_farki / min_fiyat)
        
        # Komisyon maliyeti (Alırken + Satarken = 2 işlem)
        toplam_komisyon_maliyeti = yatirim_miktari * (komisyon_orani * 2)
        
        # Brüt ve Net Kar
        brut_kar = yatirim_miktari * yuzdesel_fark
        net_kar = brut_kar - toplam_komisyon_maliyeti
        
        # --- SONUÇLARI GÖSTERME (METRİKLER) ---
        col1, col2, col3 = st.columns(3)
        col1.metric("En Düşük Fiyat (AL)", f"${min_fiyat:,.2f}", en_ucuz['Borsa'])
        col2.metric("En Yüksek Fiyat (SAT)", f"${max_fiyat:,.2f}", en_pahali['Borsa'])
        
        # Eğer Net Kar pozitifse yeşil, negatifse kırmızı göster
        delta_color = "normal" if net_kar > 0 else "inverse"
        col3.metric("Tahmini Net Kar", f"${net_kar:.2f}", f"%{(yuzdesel_fark*100):.2f} Spread", delta_color=delta_color)

        st.divider()

        # Detaylı Analiz Mesajı
        if net_kar > 0:
            st.success(f"✅ **FIRSAT VAR!** {en_ucuz['Borsa']}'dan alıp {en_pahali['Borsa']}'da satarsanız komisyonlar düşünce **${net_kar:.2f}** kar edebilirsiniz.")
        else:
            st.warning(f"⚠️ **Fırsat Yok.** Borsalar arası fiyat farkı, komisyon maliyetini (${toplam_komisyon_maliyeti:.2f}) kurtarmıyor.")

        # --- GÖRSELLEŞTİRME ---
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.subheader("Borsalara Göre Fiyat Karşılaştırması")
            st.bar_chart(df, x="Borsa", y="Fiyat ($)", color="#4CAF50") # Yeşil renkli bar chart
            
        with col_chart2:
            st.subheader("Fiyat Listesi")
            st.dataframe(df.sort_values(by="Fiyat ($)"), hide_index=True)

    else:
        st.error("Veri çekilemedi. İnternet bağlantınızı kontrol edin veya sembolü değiştirin.")

else:
    st.info("Analizi başlatmak için butona tıklayın.")