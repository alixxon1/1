#projekt - program grający kolędę "Mędrcy swiata, monarchowie"

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

#żeby ułatwić oznaczanie dźwięków, użyję notacji amerykańskiej (zwanej międzynarodową), 
#w której oktawy numeruje się od zera, a dźwięk a = 440Hz oznaczany jest jako a4

czestotliwosc_a4 = 440 #Hz

#n - liczba półtonów dzieląca dany dźwięk od dźwięku a4
#półton - najmniejsza jednostka systematyczna mierząca odległosć między dźwiękami
#jesli dźwięk będzie niższy o n półtonów od dźwięku a4, n będzie ujemne, jesli wyższy - n będzie dodatnie

def czestotliwosc(n):
    return czestotliwosc_a4 * 2**(n/12)     #wzór ogólny na częstotliwosć dźwięków względem dźwięku a = 440Hz
    
def odleglosc(dzwiek):
    
    #lista wszystkich możliwych dźwięków
    tony_krzyzyk = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'h']
    tony_bemol = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'b', 'h'] #dźwięk h z bemolem nazywa się b
    
    nazwa = dzwiek[0][:-1]
    oktawa = int(dzwiek[0][-1:])
    
    if nazwa not in tony_krzyzyk and nazwa not in tony_bemol:
        print("Błędny dźwięk")
        return
    
    if nazwa in tony_krzyzyk:
        tony = tony_krzyzyk
    else:
        tony = tony_bemol
        
    return (tony.index(nazwa) + 12 * (oktawa - 4)) - (tony.index('a'))

#tempo podawane jest na początku zapisu utworu w bpm - beats per minute

def czas_dzwieku(dzwiek, tempo):
    
    czas_uderzenia = 60/tempo  #60 sekund podzielone na tempo - podaje mi, ile sekund trwa jedno uderzenie
    
    wartosci = ['cala nuta', 'polnuta', 'cwiercnuta', 'osemka', 'szesnastka', 'trzydziestodwojka']
    
    #wartosci nut posegregowane od najdłuższej do najkrótszej: 
    #cała nuta - 4 uderzenia, półnuta - 2 ud., ćwierćnuta - 1 ud., ósemka - 1/2 ud. itd.
    
    czasy = np.zeros(len(wartosci))
    
    for i in range(len(wartosci)):
        czasy[i] = czas_uderzenia * (4/(2**i))
    
    czas_podany = dzwiek[1]
    
    #kropka przy dźwięku przedłuża jego wartosć (długosć trwania) o połowę, w celu ułatwienia nazywam dźwięki z kropką
    #ich nazwą i dopiskiem kropka, by uniknąć utrudnień w zapisie (poprawny zapis brzmiałby np. 'ćwierćnuta z kropką', 
    #zamiast zastosowanego 'ćwierćnuta kropka')
    
    if 'kropka' in czas_podany:
        czas_bez_kropki = czas_podany.replace(' kropka', '')
        if czas_bez_kropki not in wartosci:
            print("Błędna długość dźwięku")
            return
        
        for i in range(len(wartosci)):
            if czas_bez_kropki == wartosci[i]:
                czas_trwania = czasy[i] * 1.5
                return czas_trwania
        
    elif czas_podany not in wartosci:
        print("Błędna długość dźwięku")
        return
    
    else: 
        for i in range(len(wartosci)):
            if czas_podany == wartosci[i]:
                czas_trwania = czasy[i]
                return czas_trwania

#def cechy_dzwieku(dzwiek, tempo):
    
#    n = odleglosc(dzwiek)
#    return [czestotliwosc(n), czas_dzwieku(dzwiek, tempo)]

def fala_dzwiekowa(dzwiek, tempo):
    
    n = odleglosc(dzwiek)
    f = czestotliwosc(n)
    t = czas_dzwieku(dzwiek, tempo)
    
    czas = np.arange(0, t, 1/44100)
    
    fala = 0.5 * np.sin(2 * np.pi * f * czas)
    
    return czas, fala

tempo = 90

dzwieki = [['g4', 'cwiercnuta kropka'], ['ab4', 'osemka'], ['b4', 'cwiercnuta'], ['b4', 'cwiercnuta'],
           ['c5', 'cwiercnuta'], ['c5', 'cwiercnuta'], ['b4', 'cwiercnuta'], ['b4', 'cwiercnuta'],
           ['ab4', 'cwiercnuta kropka'], ['g4', 'osemka'], ['ab4', 'cwiercnuta'], ['c5', 'cwiercnuta'],
           ['b4', 'cwiercnuta kropka'], ['ab4', 'osemka'], ['g4', 'polnuta'],
           ['g4', 'cwiercnuta kropka'], ['ab4', 'osemka'], ['b4', 'cwiercnuta'], ['b4', 'cwiercnuta'],
           ['c5', 'cwiercnuta'], ['eb5', 'cwiercnuta'], ['d5', 'cwiercnuta'], ['c5', 'cwiercnuta'], 
           ['b4', 'cwiercnuta kropka'], ['g4', 'osemka'], ['ab4', 'cwiercnuta kropka'], ['f4', 'osemka'],
           ['f4', 'polnuta'], ['eb4', 'polnuta'], 
           ['f4', 'cwiercnuta kropka'], ['g4', 'osemka'], ['ab4', 'osemka'], ['b4', 'osemka'], ['c5', 'osemka'], ['d5', 'osemka'], 
           ['eb5', 'cwiercnuta'], ['g5', 'cwiercnuta'], ['eb5', 'cwiercnuta'], ['b4', 'cwiercnuta'], 
           ['ab4', 'cwiercnuta'], ['f5', 'cwiercnuta'], ['g4', 'cwiercnuta'], ['eb5', 'cwiercnuta'], 
           ['g4', 'polnuta'], ['f4', 'polnuta'], 
           ['g4', 'cwiercnuta kropka'], ['ab4', 'osemka'], ['b4', 'cwiercnuta'], ['b4', 'cwiercnuta'], 
           ['c5', 'cwiercnuta'], ['eb5', 'cwiercnuta'], ['d5', 'cwiercnuta'], ['c5', 'cwiercnuta'], 
           ['b4', 'cwiercnuta kropka'], ['g4', 'osemka'], ['ab4', 'cwiercnuta kropka'], ['f4', 'osemka'], 
           ['f4', 'polnuta'], ['eb4', 'polnuta kropka']]

czas_pokaz = 0
fala_pokaz = 0

for i in range(len(dzwieki)):
    czas, fala = fala_dzwiekowa(dzwieki[i], tempo)
    czas_pokaz += czas[:int(0.01 * 44100)]
    fala_pokaz += fala[:int(0.01 * 44100)]
    sd.play(fala, samplerate=44100)
    sd.wait()

plt.plot(czas_pokaz, fala_pokaz)
plt.title('Fala Dźwiękowa')
plt.show()