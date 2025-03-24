
from collections import defaultdict
import heapq
from typing import Dict, List, Tuple, Optional
from collections import deque

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx  # İstasyonun benzersiz kimliği
        self.ad = ad    # İstasyon adı
        self.hat = hat  # İstasyonun bulunduğu hat
        self.komsular = []  # Bu istasyona komşu olan istasyonlar (istasyon, süre) şeklinde tutulur

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        """Bu istasyona yeni bir komşu istasyon ekler."""
        self.komsular.append((istasyon, sure))

    def __lt__(self, other):
        """İstasyonları alfabetik sıralamak için karşılaştırma metodunu tanımlar."""
        return self.idx < other.idx


class MetroAgi:
    def __init__(self):
        self.istasyonlar = {}  # Tüm istasyonlar burada tutulur (id -> Istasyon)
        self.hatlar = defaultdict(list)  # Hatlar ve bu hatlar üzerindeki istasyonlar
        self.ortalama_sureler = {}  # İki istasyon arasındaki ortalama süre

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        """Yeni bir istasyon ekler."""
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        """İki istasyon arasına bağlantı ekler."""
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            print("Hatalı istasyon ID'si!")
            return

        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

        # Ortalama süreyi güncelle
        key = tuple(sorted([istasyon1_id, istasyon2_id]))
        if key in self.ortalama_sureler:
            self.ortalama_sureler[key] = (self.ortalama_sureler[key] + sure) / 2
        else:
            self.ortalama_sureler[key] = sure

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması ile en az aktarmalı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print("Geçersiz istasyonlar!")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # BFS için kuyruk oluşturuluyor
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set([baslangic])

        while kuyruk:
            current, yol = kuyruk.popleft()

            if current == hedef:
                return yol  # Hedefe ulaşıldığında rotayı döndürüyoruz

            for komsu, _ in current.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, yol + [komsu]))

        return None  # Rota bulunamazsa None döndürür

    def tahmini_sure(self, mevcut: Istasyon, hedef: Istasyon) -> float:
        """İki istasyon arasındaki ortalama süreyi tahmini olarak verir."""
        key = tuple(sorted([mevcut.idx, hedef.idx]))
        return self.ortalama_sureler.get(key, 5)  # Bilgi yoksa 5 dakika varsayılır

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması ile en hızlı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print("Geçersiz istasyonlar!")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        pq = [(0, 0, baslangic, [baslangic])]  # (gerçek süre, tahmini maliyet, istasyon, yol)
        ziyaret_edildi = {}

        while pq:
            sure, heuristik, current, yol = heapq.heappop(pq)

            if current in ziyaret_edildi and ziyaret_edildi[current] <= sure:
                continue
            ziyaret_edildi[current] = sure

            if current == hedef:
                return yol, sure  # En hızlı rotayı ve süreyi döndürür

            for komsu, komsu_sure in current.komsular:
                if komsu not in ziyaret_edildi or sure + komsu_sure < ziyaret_edildi[komsu]:
                    yeni_sure = sure + komsu_sure
                    tahmini_maliyet = yeni_sure + self.tahmini_sure(komsu, hedef)  # Ortalama süreyi heuristik olarak kullanıyoruz
                    heapq.heappush(pq, (yeni_sure, tahmini_maliyet, komsu, yol + [komsu]))

        return None  # Rota bulunamazsa None döndürür


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()

    # İstasyonlar ekleme
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")

    # Bağlantılar ekleme
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)

    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)

    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)

    # Hat aktarma bağlantıları
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)

    # Test senaryoları
    print("\n=== Test Senaryoları ===")

    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    #extra test
    print("\n4. Batıkent'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T1", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
