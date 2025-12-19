import streamlit as st
import ccxt
import pandas as pd
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Crypto Arbitraj V2", layout="wide")

st.title("⚡ Kripto Para Arbitraj Tarayıcısı")
st.markdown("""
Bu uygulama, merkezi borsalar arasındaki fiyat farklarını analiz eder.
Soldaki menüden ayarları yapıp **"Analiz Et"** butonuna basınız.
""")

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    secilen_coin = st.selectbox("Coin Seçin", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "AVAX/USDT"])
    
    st.divider()
    
    yatirim_miktari = st.number_input("Yatırım Miktarı ($)", min_value=100, value=1000, step=100)
    
    # Komisyonu senin istediğin gibi hassas girebilmek için number_input yaptık
    # Format '%.3f' virgülden sonra 3 basamak gösterir.
    komisyon_yuzdesi = st.number_input("Borsa Komisyonu (%)", min_value=0.0, value=0.1, step=0.01, format="%.3f")
    komisyon_orani = komisyon_yuzdesi / 100
    
    st.divider()
    
    # BUTON ARTIK BURADA!
    analiz_butonu = st.button("🚀 Fiyatları Tara ve Analiz Et", use_container_width=True)

# --- FONKSİYONLAR ---
def fiyatlari_getir(symbol):
    # Daha fazla borsa ekledim şans artması için
    borsalar = [ccxt.binance(), ccxt.kraken(), ccxt.coinbase(), ccxt.kucoin(), ccxt.bitstamp()]
    veri_listesi = []

    # Progress bar ana ekranda çıksın
    durum_metni = st.empty()
    my_bar = st.progress(0)
    step = 100 / len(borsalar)
    
    for i, borsa in enumerate(borsalar):
        try:
            durum_metni.text(f"{borsa.name} taranıyor...")
            
            # Sembol düzeltme mantığı (USDT/USD)
            arama_sembolu = symbol
            if borsa.id in ['kraken', 'coinbase', 'bitstamp'] and symbol.endswith('USDT'):
                arama_sembolu = symbol.replace('USDT', 'USD')
            
            ticker = borsa.fetch_ticker(arama_sembolu)
            fiyat = ticker['last']
            
            veri_listesi.append({
                "Borsa": borsa.name,
                "Fiyat ($)": float(fiyat),
                "Sembol": arama_sembolu
            })
        except Exception:
            pass # Hata veren borsayı atla
        finally:
            my_bar.progress(int((i + 1) * step))
            
    my_bar.empty()
    durum_metni.empty()
    return pd.DataFrame(veri_listesi)

# Tabloda Min/Max renklendirmesi için yardımcı fonksiyon
def renklendir(val, min_val, max_val):
    if val == min_val:
        return 'background-color: #d4edda; color: green; font-weight: bold' # Yeşil (Ucuz)
    elif val == max_val:
        return 'background-color: #f8d7da; color: red; font-weight: bold'   # Kırmızı (Pahalı)
    return ''

# --- ANA AKIŞ ---

if analiz_butonu: # Sidebar'daki butona basıldıysa
    with st.spinner('Piyasalar taranıyor...'):
        df = fiyatlari_getir(secilen_coin)
    
    if not df.empty:
        # En ucuz ve En pahalıyı bulma
        en_ucuz_row = df.loc[df['Fiyat ($)'].idxmin()]
        en_pahali_row = df.loc[df['Fiyat ($)'].idxmax()]
        
        min_fiyat = en_ucuz_row['Fiyat ($)']
        max_fiyat = en_pahali_row['Fiyat ($)']
        
        # Hesaplamalar
        fiyat_farki = max_fiyat - min_fiyat
        yuzdesel_fark = (fiyat_farki / min_fiyat)
        toplam_komisyon = yatirim_miktari * (komisyon_orani * 2)
        brut_kar = yatirim_miktari * yuzdesel_fark
        net_kar = brut_kar - toplam_komisyon
        
        # --- METRİKLER ---
        st.subheader("📊 Analiz Sonuçları")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("En Ucuz (AL)", f"${min_fiyat:,.2f}", en_ucuz_row['Borsa'])
        c2.metric("En Pahalı (SAT)", f"${max_fiyat:,.2f}", en_pahali_row['Borsa'])
        c3.metric("Fiyat Farkı (Spread)", f"%{(yuzdesel_fark*100):.2f}")
        
        delta_color = "normal" if net_kar > 0 else "inverse"
        c4.metric("Net Kar", f"${net_kar:.2f}", delta_color=delta_color)

        st.divider()

        if net_kar > 0:
            st.success(f"✅ **ARBITRAJ FIRSATI!** {en_ucuz_row['Borsa']} borsasından alıp {en_pahali_row['Borsa']} borsasında satarak komisyonlar düşüldükten sonra **${net_kar:.2f}** kazanabilirsiniz.")
        else:
            st.warning(f"⚠️ **Fırsat Yok.** {en_ucuz_row['Borsa']} ve {en_pahali_row['Borsa']} arasındaki fark komisyonları (${toplam_komisyon:.2f}) karşılamıyor.")

        # --- GÖRSELLEŞTİRME VE TABLO ---
        col_grafik, col_tablo = st.columns([1, 1])
        
        with col_grafik:
            st.caption("Fiyat Karşılaştırması")
            st.bar_chart(df.set_index("Borsa")["Fiyat ($)"])
            
        with col_tablo:
            st.caption("Detaylı Fiyat Listesi")
            # Pandas Styler kullanarak renklendirme yapıyoruz (Mühendis dokunuşu)
            st.dataframe(
                df.style.format({"Fiyat ($)": "{:.2f}"})
                  .applymap(lambda x: renklendir(x, min_fiyat, max_fiyat), subset=['Fiyat ($)']),
                use_container_width=True
            )

    else:
        st.error("Veri çekilemedi. Lütfen bağlantınızı kontrol edin.")

else:
    # Sayfa ilk açıldığında boş kalmasın diye karşılama ekranı
    st.info("👈 Başlamak için sol menüden 'Analiz Et' butonuna tıklayın.")