### Weather Analysis Dashboard ###

Bu proje, Python kullanarak belirlenen bir şehir için detaylı hava durumu analizi yapan ve verileri görselleştiren bir araçtır. OpenWeatherMap API kullanılarak veriler çekilir ve Matplotlib ile görselleştirilir.

# Özellikler (Mevcut Durum)
- **API Entegrasyonu:** Anlık ve 7 günlük hava durumu verisi çekme.
- **Veri Analizi:** Günlük ortalama sıcaklıklar ve hissedilen sıcaklık hesaplamaları.
- **Görselleştirme:**
  -  **Saatlik:** Çizgi grafik (Line Chart) ile gün içi sıcaklık değişimi.
  -  **Haftalık:** Sütun grafik (Bar Chart) ile 7 günlük ortalama sıcaklıklar.
- **CLI Arayüzü:** Terminal üzerinden kullanıcı etkileşimi.

# Kullanılan Teknolojiler
- Python 3.x
- Matplotlib (Görselleştirme)
- Requests (API İstekleri)
- Python-Dotenv (Çevresel Değişkenler)

# Gelecek Hedefler (Roadmap)
- [ ] Projenin Masaüstü CLI halinden **Web GUI**'ye taşınması (Django/Flask).
- [ ] Verilerin veritabanına kaydedilmesi (SQL).
- [ ] Daha detaylı istatistiksel analizlerin eklenmesi.

# Kurulum

1. Repoyu klonlayın.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt