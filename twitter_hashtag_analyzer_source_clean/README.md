# Twitter Hashtag Analiz Aracı

Bu proje, Twitter'daki hashtag'leri analiz eden ve katılımcıların coğrafi dağılımını harita üzerinde gösteren bir web uygulamasıdır.

## Özellikler

1. **Hashtag Arama**: Herhangi bir Twitter hashtag'ini analiz edebilirsiniz.

2. **Özet İstatistikler**:
   - Toplam tweet sayısı
   - Toplam katılımcı sayısı
   - Tweet türleri dağılımı (orijinal, retweet, yanıt, medya)
   - Duygu analizi skoru

3. **Aktivite Grafiği**:
   - Zaman içindeki tweet aktivitesini gösteren çizgi grafiği
   - Tweet türlerine göre ayrıştırılmış veriler

4. **Duygu Analizi**:
   - Genel duygu skoru
   - Olumlu/olumsuz/nötr dağılımı pasta grafiği
   - Zaman içindeki duygu değişimi grafiği

5. **En Aktif Katılımcılar**:
   - En çok tweet atan kullanıcılar
   - Etki puanı ve takipçi sayılarıyla birlikte

6. **Coğrafi Dağılım Haritası**:
   - Katılımcıların dünya haritası üzerindeki dağılımı
   - İki görünüm modu: Isı haritası ve işaretçiler
   - Ülke bazlı filtreleme özelliği
   - Ülkelere göre dağılım pasta grafiği
   - En çok katılımcı olan konumların listesi

## Proje Yapısı

### Backend

- `backend/models/`: Veritabanı modelleri
- `backend/services/`: Twitter API, duygu analizi ve konum servisleri
- `backend/utils/`: Yardımcı fonksiyonlar
- `backend/hashtag_analyzer.py`: Ana analiz motoru
- `backend/create_test_data.py`: Test verileri oluşturma scripti

### Frontend

- `frontend/src/components/`: React bileşenleri
- `frontend/src/App.js`: Ana uygulama bileşeni
- `frontend/src/App.css`: Stil dosyası

## Kurulum

### Backend Kurulumu

1. Python 3.6+ gereklidir
2. Gerekli paketleri yükleyin:
   ```
   pip install textblob requests sqlite3
   ```
3. Test veritabanını oluşturun:
   ```
   cd backend
   python create_test_data.py
   ```

### Frontend Kurulumu

1. Node.js 14+ gereklidir
2. Bağımlılıkları yükleyin:
   ```
   cd frontend
   npm install
   ```
3. Geliştirme sunucusunu başlatın:
   ```
   npm run dev
   ```

## Kullanım

1. Frontend geliştirme sunucusunu başlatın
2. Tarayıcınızda `http://localhost:5173` adresine gidin
3. Arama çubuğuna bir hashtag girin ve "Analiz Et" düğmesine tıklayın
4. Farklı sekmeleri kullanarak çeşitli analiz sonuçlarını görüntüleyin

## Örnek Veri

Proje, "#TürkiyedeKadınOlmak" hashtag'i için örnek verilerle birlikte gelir. Bu veriler, uygulamanın tüm özelliklerini test etmenizi sağlar.

## Notlar

- Gerçek zamanlı Twitter verilerini çekmek için Twitter API anahtarlarının yapılandırılması gerekir.
- Şu anki haliyle uygulama, örnek verilerle çalışmaktadır.
