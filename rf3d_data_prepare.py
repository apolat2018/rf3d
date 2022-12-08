### -*- coding: cp1254 -*-
###Dr.Ali POLAT(2018)
import arcpy,os,sys
from arcpy.sa import *
from arcpy import env
reload(sys)
sys.setdefaultencoding("utf8")
arcpy.env.overwriteOutput = True

folder=arcpy.GetParameterAsText(0)
dem=arcpy.GetParameterAsText(1)
st=arcpy.GetParameterAsText(2)
rocks=arcpy.GetParameterAsText(3)
density=arcpy.GetParameterAsText(4)
cellsize=arcpy.GetParameterAsText(5)

rock_net=arcpy.GetParameterAsText(6)
arcpy.AddMessage(rock_net)

    
arcpy.env.extent =dem
arcpy.CreateFolder_management(folder,"temp")
ws=folder+"/"+"temp"
arcpy.env.workspace=ws
arcpy.AddMessage(ws)


dem_min=BlockStatistics(dem,NbrRectangle(4,4,"CELL"),"MINIMUM")
dem_min.save(ws+"\dem_min")
arcpy.AddMessage("Minumun Dem ulu�turuluyor")
dem_mean=BlockStatistics(dem,NbrRectangle(4,4,"CELL"),"MEAN")
dem_mean.save(ws+"\dem_mean")
arcpy.AddMessage("Mean Dem ulu�turuluyor")

arcpy.AddMessage("RG dosyas� olu�turuluyor")
roughness=dem_mean-dem_min
roughness.save(ws+"/rg.tif")

arcpy.AddMessage("S�n�fland�rma dosyas� olu�turuluyor")
arcpy.env.extent=roughness
rec_rg=Reclassify(roughness,"VALUE",RemapRange([[0,0.1,1],[0.1,0.5,2],[0.5,1,3],[1,2.5,4],[2.5,10,5],[10,100,6]]),"NODATA")
rec_rg.save(ws+"/rec_rg.tif")

##Zemin tiplerini ayri ayri boluyor

del_fields0 = [c.name for c in arcpy.ListFields(st) if not c.required]
if len(del_fields0)>1:

    for b in del_fields0:
        arcpy.AddMessage("silinecekler: "+b)
        arcpy.AddMessage(len(del_fields0))
        if b=="soiltype":
            d=del_fields0.index("soiltype")
            del del_fields0[d]
        else:
            del del_fields0[1]
    arcpy.AddMessage(del_fields0)
    arcpy.DeleteField_management(st, del_fields0)
        

arcpy.AddField_management(st,"rg70","DOUBLE")
arcpy.AddField_management(st,"rg20","DOUBLE")
arcpy.AddField_management(st,"rg10","DOUBLE")
arcpy.AddMessage("Zemin tipleri ayri ayri kaydediliyor")


with arcpy.da.SearchCursor(st,"soiltype") as scr:
    for row in scr:
        if row[0]==0:
            arcpy.AddMessage("ST_0 Kaydediliyor")
            arcpy.Select_analysis(st,"st_0.shp",'"soiltype" = 0')
        elif row[0]==1:
            arcpy.AddMessage("ST_1 Kaydediliyor")
            arcpy.Select_analysis(st,"st_1.shp",'"soiltype" = 1')
        elif row[0]==2:
            arcpy.AddMessage("ST_2 Kaydediliyor")
            arcpy.Select_analysis(st,"st_2.shp",'"soiltype" = 2')
        elif row[0]==3:
            arcpy.AddMessage("ST_3 Kaydediliyor")
            arcpy.Select_analysis(st,"st_3.shp",'"soiltype" = 3')   
        elif row[0]==4:
            arcpy.AddMessage("ST_4 Kaydediliyor")
            arcpy.Select_analysis(st,"st_4.shp",'"soiltype" = 4')
        elif row[0]==5:
            arcpy.AddMessage("ST_5 Kaydediliyor")
            arcpy.Select_analysis(st,"st_5.shp",'"soiltype" = 5')
        elif row[0]==6:
            arcpy.AddMessage("ST_6 Kaydediliyor")
            arcpy.Select_analysis(st,"st_6.shp",'"soiltype" = 6')
        elif row[0]==7:
            arcpy.AddMessage("ST_7 Kaydediliyor")
            arcpy.Select_analysis(st,"st_7.shp",'"soiltype" = 7')


##Masking
arcpy.env.ext=rec_rg.extent           
mask_data=arcpy.ListFiles("st_*.shp")
for i in mask_data:
   
    ad=str(i)
    ad.split()
    arcpy.AddMessage(ad[0:4])
    ext=ExtractByMask(rec_rg,i)
    ext.save(ws+"/"+ad[0:4]+"ext.tif")



rec_data=arcpy.ListFiles("st_*.tif")

##Raster lar tabloya donusturuluyor
for j in rec_data:
    ad2=str(j)
    ad2.split()
    adi="tbl_"+ad2[0:4]+".dbf"
    adi2="znl_"+ad2[0:4]+".dbf"
    arcpy.AddMessage(adi)
    arcpy.TableToTable_conversion(j,ws,adi)
    ZonalStatisticsAsTable(j,"Value",roughness,adi2,"NODATA","ALL")


table_data=arcpy.ListFiles("tbl_*.dbf")
znl_data=arcpy.ListFiles("znl_*.dbf")
for j,k in zip(table_data,znl_data):
    arcpy.JoinField_management(j,"Value",k,"Value")
flds="value","count"
for k in table_data:
    arcpy.AddField_management(k,"yuzde","LONG")
    arcpy.AddField_management(k,"rg70","DOUBLE")
    arcpy.AddField_management(k,"rg20","DOUBLE")
    arcpy.AddField_management(k,"rg10","DOUBLE")
    with arcpy.da.UpdateCursor(k,flds) as upcur:
        for row1 in upcur:
            if row1[0]<0:
                row1[1]=0
                upcur.updateRow(row1)

lst_0=[]
lst_1=[]
lst_2=[]
lst_3=[]
lst_4=[]
lst_5=[]
lst_6=[]
lst_7=[]

lst_0m=[]
lst_1m=[]
lst_2m=[]
lst_3m=[]
lst_4m=[]
lst_5m=[]
lst_6m=[]
lst_7m=[]

lst_0y=[]
lst_1y=[]
lst_2y=[]
lst_3y=[]
lst_4y=[]
lst_5y=[]
lst_6y=[]
lst_7y=[]

fs="count","yuzde","mean","rg70","rg20","rg10"
st_flds="soiltype","rg10","rg20","rg70"
for l in table_data:
    ls=str(l)
    ls.split()
    st1=ls[7]
    arcpy.AddMessage(st1)
    
    if l=="tbl_st_0.dbf":#Zemin tipi 0 ise Rg degerleri 100 olacak
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==0:
                    row[1]=100
                    row[2]=100
                    row[3]=100
                    ap.updateRow(row)
                del row
            del ap

        
    elif l=="tbl_st_1.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_1.append(row[0])
                lst_1m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_1=sum(lst_1)
                row[1]=(100*row[0])/toplam_1
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_1y.append(row[1])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:                      
                r70=[]
                r20=[]
                r10=[]
                for k in lst_0y:
                   
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_1m[sira70]
                rg20=lst_1m[sira20]
                rg10=lst_1m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==1:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_2.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_2.append(row[0])
                lst_2m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_2=sum(lst_2)
                row[1]=(100*row[0])/toplam_2
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_2.append(row[0])
                lst_2y.append(row[1])
                lst_2m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_2y:
                    
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_2m[sira70]
                rg20=lst_2m[sira20]
                rg10=lst_2m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==2:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_3.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_3.append(row[0])
                lst_3m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_3=sum(lst_3)
                row[1]=(100*row[0])/toplam_3
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_3.append(row[0])
                lst_3y.append(row[1])
                lst_3m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_3y:
                    
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_3m[sira70]
                rg20=lst_3m[sira20]
                rg10=lst_3m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==3:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_4.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_4.append(row[0])
                lst_4m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_4=sum(lst_4)
                row[1]=(100*row[0])/toplam_4
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_4.append(row[0])
                lst_4y.append(row[1])
                lst_4m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_4y:
                   
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_4m[sira70]
                rg20=lst_4m[sira20]
                rg10=lst_4m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==4:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_5.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_5.append(row[0])
                lst_5m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_5=sum(lst_5)
                row[1]=(100*row[0])/toplam_5
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_5.append(row[0])
                lst_5y.append(row[1])
                lst_5m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_5y:
                   
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_5m[sira70]
                rg20=lst_5m[sira20]
                rg10=lst_5m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==5:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_6.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_6.append(row[0])
                lst_6m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_6=sum(lst_6)
                row[1]=(100*row[0])/toplam_6
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_6.append(row[0])
                lst_6y.append(row[1])
                lst_6m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_6y:
                    
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_6m[sira70]
                rg20=lst_6m[sira20]
                rg10=lst_6m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==6:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    elif l=="tbl_st_7.dbf":
        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_7.append(row[0])
                lst_7m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                toplam_7=sum(lst_7)
                row[1]=(100*row[0])/toplam_7
                ap.updateRow(row)
                del row
            del ap

        with arcpy.da.SearchCursor(l,fs) as sc:
            for row in sc:
                lst_7.append(row[0])
                lst_7y.append(row[1])
                lst_7m.append(row[2])
                del row
            del sc
        with arcpy.da.UpdateCursor(l,fs) as ap:
            for row in ap:
                r70=[]
                r20=[]
                r10=[]
                for k in lst_7y:
                    x=70-k
                    y=20-k
                    z=10-k
                    r70.append(abs(x))
                    r20.append(abs(y))
                    r10.append(abs(z))
                mn70=min(r70)
                sira70=r70.index(mn70)
                mn20=min(r20)
                sira20=r20.index(mn20)
                mn10=min(r10)
                sira10=r10.index(mn10)
                rg70=lst_7m[sira70]
                rg20=lst_7m[sira20]
                rg10=lst_7m[sira10]
                row[3]=rg70
                row[4]=rg20
                row[5]=rg10
                        
                            
                ap.updateRow(row)
                del row
                
            del ap
        with arcpy.da.UpdateCursor(st,st_flds) as ap:
            for row in ap:
                if row[0]==7:
                    row[1]=rg10
                    row[2]=rg20
                    row[3]=rg70
                ap.updateRow(row)
                del row
            del ap
    else:
        arcpy.AddMessage("HATA")

snfla="""def sinifla(deger):#bulunan arazi pürüzlülüğü değerleri RF3Dnin istediği değerlere dönüştürülüyor,,,,deger rg değeri field ise bu değern yazılacağı tablodaki alan
    rgs=[0,0.03, 0.05, 0.08, 0.1,0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,1.1, 1.2, 1.3, 1.4, 1.5, 2, 2.5,3, 4, 5, 6, 7, 8, 9, 10,100]
    check_1=[]
    for i in rgs:
        s=abs(deger-i)
        check_1.append(s)
    
    indx=check_1.index(min(check_1))
    x=rgs[indx]
    return x"""   

arcpy.CalculateField_management(st,"rg70","sinifla(!rg70!)","PYTHON",snfla)
arcpy.CalculateField_management(st,"rg20","sinifla(!rg20!)","PYTHON",snfla)
arcpy.CalculateField_management(st,"rg10","sinifla(!rg10!)","PYTHON",snfla)
##Cell Size ayarlayalim
arcpy.env.extent=dem
arcpy.env.cellSize = cellsize

rg10ras=arcpy.PolygonToRaster_conversion(st,"rg10","rg10ras","CELL_CENTER","",cellsize)
rg20ras=arcpy.PolygonToRaster_conversion(st,"rg20","rg20ras","CELL_CENTER","",cellsize)
rg70ras=arcpy.PolygonToRaster_conversion(st,"rg70","rg70ras","CELL_CENTER","",cellsize)
soilras=arcpy.PolygonToRaster_conversion(st,"soiltype","soilras","CELL_CENTER","",cellsize)

arcpy.env.workspace=folder

##ASC formatinda kaydettigimizde decimal ayraci virgul oluyor bu yuzden TXT kaydedecegiz
arcpy.RasterToASCII_conversion(rg10ras,"rg10.txt")
arcpy.RasterToASCII_conversion(rg20ras,"rg20.txt")
arcpy.RasterToASCII_conversion(rg70ras,"rg70.txt")
arcpy.RasterToASCII_conversion(soilras,"soiltype.txt")

##.....................................................................................
## ROCKS Shapes Calculating
arcpy.AddMessage("CALCULATING ROCKS SHAPES")

arcpy.env.workspace=ws

    

##Rocks tablosu alanlarin hepsi siliniyor nid alani ekleniyor sadece nid alaninin kalmasi saglaniyor

del_fields = [b.name for b in arcpy.ListFields(rocks) if not b.required]
arcpy.AddMessage(del_fields)

bak="".join(del_fields)
arcpy.AddMessage(bak)
ara=bak.find("NID")
arcpy.AddMessage(ara)

if ara != -1:
    arcpy.AddMessage(del_fields)
    nsira=del_fields.index("NID")
    del del_fields[nsira]
    arcpy.DeleteField_management(rocks, del_fields)
   
    
else:
    arcpy.AddField_management(rocks,"NID","SHORT")
    del_fields = [b.name for b in arcpy.ListFields(rocks) if not b.required]
    arcpy.AddMessage(del_fields)
    nsira1=del_fields.index("NID")
    del del_fields[nsira1]
    arcpy.DeleteField_management(rocks, del_fields)
    
block="""rec=0
def yaz():
    global rec
    pstart=1
    pinterval=1
    if(rec==0):
        rec=pstart
    else:
        rec+=pinterval
    return rec"""
expression="yaz()"


arcpy.AddField_management(rocks,"d1","DOUBLE")
arcpy.AddField_management(rocks,"d2","DOUBLE")
arcpy.AddField_management(rocks,"d3","DOUBLE")
arcpy.AddField_management(rocks,"yogunluk","DOUBLE")
arcpy.AddField_management(rocks,"blshape","SHORT")
arcpy.AddField_management(rocks,"density","DOUBLE")
arcpy.CalculateField_management(rocks,"NID",expression,"PYTHON",block)
arcpy.CalculateField_management(rocks,"density",density,"PYTHON")##Kayaclarin yogunlugu

arcpy.AddGeometryAttributes_management(rocks,"PERIMETER_LENGTH","METERS","SQUARE_METERS","")
arcpy.AddGeometryAttributes_management(rocks,"AREA","METERS","SQUARE_METERS","")
arcpy.CalculateField_management(rocks,"yogunluk","!POLY_AREA!/math.pow(!PERIMETER!,2)","PYTHON")


arcpy.MinimumBoundingGeometry_management(rocks,"mbg.shp","RECTANGLE_BY_WIDTH","NONE","","MBG_FIELDS")
arcpy.CalculateField_management("mbg.shp","d2",'!MBG_Width!',"PYTHON")
arcpy.CalculateField_management("mbg.shp","d3",'!MBG_Length!',"PYTHON")



##Kayalarin yukseklikleri hesaplaniyor
arcpy.env.cellSize = dem

arcpy.AddMessage("CALCULATING h values")
ZonalStatisticsAsTable(rocks,"NID",dem,"zonal.dbf","NODATA","ALL")
arcpy.AddField_management("zonal.dbf","h","DOUBLE")
arcpy.CalculateField_management("zonal.dbf","h",'!MEAN!-!MIN!',"PYTHON")

arcpy.env.cellSize = cellsize
##Yukseklikler kontrol ediliyor hata olanlara 1 yazacak
arcpy.AddMessage("CHECKING h values")
block2="""
def bak(a,b):
    if(a>b):
        return 1
    else:
        return 0"""

arcpy.AddMessage("JOINING tables")

arcpy.JoinField_management("mbg.shp","NID","zonal.dbf","NID","h")
arcpy.CalculateField_management("mbg.shp","d1",'!h!',"PYTHON")
arcpy.AddField_management("mbg.shp","test","SHORT")
arcpy.CalculateField_management("mbg.shp","test",'bak(!d1!,!d2!)',"PYTHON",block2)

arcpy.AddField_management("mbg.shp","en_boy","DOUBLE")
arcpy.AddField_management("mbg.shp","h_en","DOUBLE")
arcpy.AddField_management("mbg.shp","elips_alan","DOUBLE")
arcpy.AddField_management("mbg.shp","mbg_alan","DOUBLE")
arcpy.CalculateField_management("mbg.shp","h_en",'!d1!/!d2!',"PYTHON")
arcpy.CalculateField_management("mbg.shp","en_boy",'!d2!/!d3!',"PYTHON")
arcpy.CalculateField_management("mbg.shp","mbg_alan",'!d2!*!d3!',"PYTHON")
arcpy.CalculateField_management("mbg.shp","elips_alan",'math.pi*(!d2!/2)*(!d3!/2)',"PYTHON")

##disk sekilli bloklar belirleniyor

arcpy.AddMessage("DEFINING block shapes")
block_disk="""def disk(a,b,c):
    array=[a,b,c]
    tmin=min(array)
    x=a/3
    y=b/3
    z=c/3
    if (tmin==a and tmin<y and tmin<z):
       return 4    
    elif (tmin==b and tmin<x and tmin<z):
       return 4
    elif (tmin==c and tmin<x and tmin<y):
       return 4
    
    else:
        return 0"""
      
arcpy.CalculateField_management("mbg.shp","blshape",'disk(!d1!,!d2!,!d3!)',"PYTHON",block_disk)


fields_del="yogunluk","POLY_AREA","d1","d2","d3","blshape","test"
arcpy.DeleteField_management(rocks, fields_del)
j_fields="POLY_AREA","mbg_alan","elips_alan","d1","d2","d3","blshape","density","test","yogunluk","en_boy","h_en"
arcpy.JoinField_management(rocks,"NID","mbg.shp","NID",j_fields)
arcpy.AddField_management(rocks,"ao","DOUBLE")
arcpy.CalculateField_management(rocks,"ao",'!POLY_AREA!/!mbg_alan!',"PYTHON")
##kure olan bloklar belirleniyor
block_kure="""def kure(bs,eb,he,yog):
    if (bs==0 and eb>=0.8 and he>=0.8 and yog>=0.07):
        return 3
    else:
        return bs"""

arcpy.CalculateField_management(rocks,"blshape",'kure(!blshape!,!en_boy!,!h_en!,!yogunluk!)',"PYTHON",block_kure)




##elips ve dikdortgen olan bloklar belirleniyor
up_fields="ao","yogunluk","h_en","en_boy","blshape"


with arcpy.da.UpdateCursor(rocks,up_fields) as upcursor:
        for row in upcursor:
            if(row[0]<=0.8 and row[1]>=0.065 and row[2]<=0.9 and row[3]<=0.9 and row[4]!=4 and row[4]!=3):
                row[4]=2
            
            upcursor.updateRow(row)

with arcpy.da.UpdateCursor(rocks,up_fields) as upcursor1:
        for row1 in upcursor1:
            if(row1[4]<2):
                row1[4]=1
            
            upcursor1.updateRow(row1)
            
        

bls=arcpy.PolygonToRaster_conversion(rocks,"blshape","blshape.tif","CELL_CENTER")
d1=arcpy.PolygonToRaster_conversion(rocks,"d1","d1.tif","CELL_CENTER")
d2=arcpy.PolygonToRaster_conversion(rocks,"d2","d2.tif","CELL_CENTER")
d3=arcpy.PolygonToRaster_conversion(rocks,"d3","d3.tif","CELL_CENTER")
dens=arcpy.PolygonToRaster_conversion(rocks,"density","density.tif","CELL_CENTER")
if rock_net =="#" or not rock_net:
    arcpy.AddMessage("No ROCK_NET file")
else:
    rn_number=arcpy.PolylineToRaster_conversion(rock_net,"net_number","net_number.tif","MAXIMUM_LENGTH")
    rn_energy=arcpy.PolylineToRaster_conversion(rock_net,"net_energy","net_energy.tif","MAXIMUM_LENGTH")
    rn_height=arcpy.PolylineToRaster_conversion(rock_net,"net_height","net_height.tif","MAXIMUM_LENGTH")
                     
    

resampled_dem=arcpy.Resample_management(dem, "dem_r.tif", cellsize, "CUBIC")

arcpy.env.workspace=folder
arcpy.env.extent=dem
arcpy.env.cellSize = cellsize

arcpy.AddMessage("CREATING ASCII Files......")
arcpy.env.cellSize = cellsize
arcpy.RasterToASCII_conversion(resampled_dem,"dem.txt")
arcpy.RasterToASCII_conversion(bls,"blshape.txt")
arcpy.RasterToASCII_conversion(d1,"d1.txt")
arcpy.RasterToASCII_conversion(d2,"d2.txt")
arcpy.RasterToASCII_conversion(d2,"d3.txt")
arcpy.RasterToASCII_conversion(dens,"rockdensity.txt")
if rock_net == "#" or not rock_net:
    arcpy.AddMessage("NO ROCK_NET data input")
else:
    arcpy.RasterToASCII_conversion(rn_number,"net_number.txt")
    arcpy.RasterToASCII_conversion(rn_energy,"net_energy.txt")
    arcpy.RasterToASCII_conversion(rn_height,"net_height.txt")



txt_files=arcpy.ListFiles("*.txt")

for n in txt_files:
    u=str(n)
    q=u.split(".")
    out=q[0]+".asc"
    fldr=folder+"/"+n
    with open (fldr,'r+')as f:
        text=f.read()
        f.seek(0)
        f.truncate()
        f.write(text.replace(",","."))
    txt=os.path.join(folder,n)
    asc=os.path.join(folder,out)
    os.rename(txt,asc)
asc_files=arcpy.ListFiles("*.asc")

for f in asc_files:
    arcpy.AddMessage(f+" is Created")
    
    


##temp klasor siliniyor

klasor_sil=folder+"/"+"temp"
## Silmekten vazgectimmmmmm



##from shutil import rmtree
##rmtree(klasor_sil)
##
##if os.path.exists:
##    arcpy.AddMessage("BIR SORUN VAR temp DOSYALARI S�LEMED�M")
##else:
##    arcpy.AddMessage("GEC�C� DOSYALAR DA S�L�ND�_ HER �EY YOLUNDA")

arcpy.AddMessage(" .............................FINISHED.............................")

