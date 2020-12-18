Base.py - Prvni pokus z praci s detekci objektu. 
Nyni uz kompletne nahrazeno skriptem PictureObjectDetection.

PictureObjectDetection.py - obsahuje třídu Object_detection.
Tato třida dokaže ve v obrazku vyhledatvat objekty.

VideoDetect.py - scrip ktery se napoji na webcameru a dela na ni detekci objektu.
Nyni nahrazen scriptem WebCamDetect.py

WebCamDetect.py - Dela to same jako VideoDetect.py. 
Využiva však pro detekci script PictureObjectDetection.py a tedy na nem zavisi
V tomto scriptu se delaly vice-vlaknove testy

WebCamDetect.py - Dela to same jako VideoDetect.py. 
Využiva však pro detekci script PictureObjectDetection.py a tedy na nem zavisi

VideoFileDetect.py - Provadi detekci objektu na videem.
Pro urychleni prace ji provadi pouze nad kazdym 10tym snimkem.

DistanceMeasure.py - Testovaci script pro detekci objektu v obrazku a mereni jeho vzdalenosti

VideoFileBackgroundSubstration.py
Použití metody odstranění pozadí na video

Pro vsechny scripty plati ze pro jejich spravne ukonceni je treba stiknout klavesu "q"
Potrebna data si scripty berou ze slozky Data ktera neni soucasti programu.

