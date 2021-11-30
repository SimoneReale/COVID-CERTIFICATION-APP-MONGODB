import random as rm
import numpy as np


colore_occhi = ('azzurri', 'verdi', 'castani', 'neri', 'ambra', 'blu', 'rossi' )

colore_capelli = ('rossi', 'neri', 'castani', 'biondi', 'giallo paglierino', 'castano scuro', 'ramati', 'bianchi')

tipo_fisico = ('magro', 'slanciato', 'grasso', 'sportivo', 'malaticcio', 'allenato', 'possente', 'difficile da descrivere', 'armonioso', 'deforme')



def returnFraseDescrizione():
    list_car = []

    list_car.append(f"Possiede degli occhi {rm.choice(colore_occhi)}")
    list_car.append(f"Sfoggia dei capelli {rm.choice(colore_capelli)}")
    list_car.append(f"Ha un fisico {rm.choice(tipo_fisico)}")
    list_car.append(f"Ha un'altezza pari a circa {abs(int(np.random.normal(170, 20)))} cm")

    rm.shuffle(list_car)

    return '\n'.join(list_car)

    