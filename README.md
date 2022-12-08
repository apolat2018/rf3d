# RockyFor3D için veri hazırlama python betiği (script)

### Nasıl kullanılır?
Bu script ArcGIS yazılımı içinde bir araç(tool) olarak kullanılabildiği gibi python betiği olarak da çalıştırılabilir.
ArcGIS yazılımında kullanmak için;
- RF3D_Tool.tbx dosyasını ve rf3d_data_prepare dosyasını bir klasöre indiriniz.
- ArcGIS yazılımını açınız.
- ArcCatalog kısmından aracı indirdiğiniz klasorü (connect to folder seçeneği ile) cataloğa dahil ediniz.
<img src="https://github.com/apolat2018/rf3d/blob/master/connect_To_folder.PNG" alt="connect to folder"/>
- indirdiğiniz arac alet kutusu şeklinde gözükecektir.
- Bu şeklin altında "input_Data_Prepretaion_for_RF3D" adlı script dosyasını görmeniz lazım.

<img src="https://github.com/apolat2018/rf3d/blob/master/tool.PNG" alt="ToolBox"/>

- Bu dosyanın üzerinde sağ tuşu tıklayınız.
- Properties menüsünü açarak açılan pencerede source kısmına indirmiş olduğunuz rf3d_data_prepare.py uzantılı dosyayı seçiniz.

OK

- input_Data_Prepretaion_for_RF3D scriptini çift tıklayarak çalıştırınız.

<img src="https://github.com/apolat2018/rf3d/blob/master/parameter.PNG" alt="parameters"/>

Gerekli parametreleri girdikten sonra OK butonu na basarak işlemi tamamlayabilirsiniz.

#### Yazılımı test etmek için demo_veri klasörü içerisine yükseklik (dem), zemin türleri (st.shp) ve kaya (rocks.shp) dosyaları eklenmiştir.

Kolay gelsin; İyi çalışmalar.

Detaylı bilgi ve kaynak göstermek için:
https://doi.org/10.17482/uumfd.769109

Doç.Dr.Ali POLAT
polatbey@gmail.com

