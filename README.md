YoloObjDet.py - Spousteci skript na kterem bezi program. 
Obsahuje tridu Speed meter ktera se spousti funkci "run"
Jsou dve moznosti spousteni. Rozdil je ve zpusobu trackovani vozidla. 
Prvni vyuziva euklidovskou vzdalenost, druhy pouzivat opticky proud.

tracker.py - obsahuje třidu EuclideanDistTracker a OpticalFlowTracker.
Jsou to třídy určené pro trackování vozidel.
Rozdíl je ve způsobu trackování vozidel jak bylo popsáno výše

LPFinder.py - funkce pro vyhledání vhodného bodu pro sledování v optickém proudu

LPTest.py - testovací skript pro LPFinder

PictureObjectDetection.py - obsahuje třídu object_detection. Třída slouží pro
detekci objektů v obraze.

Slozka Code Tests obsahuje pokusne kody na kterych byla testovani jejich funkcnost
Na funci konecneho programu nemaji zadny vliv

Pro vsechny scripty plati ze pro jejich spravne ukonceni je treba stiknout klavesu "q"
Potrebna data si scripty berou ze slozky Data ktera neni soucasti programu.

