from enum import Enum

class PLC:
    class ipPLC(Enum):
        PLC1 = "192.168.40.13"
        PLC2 = "192.168.40.14"
        PLC3 = "192.168.40.15"

    def __init__(self):
        self.acceso=False
        self.blocco=False
        self.regime=False
        self.wTermico=False
        self.wAnomaliaNastro=False
        self.wMancanzaProdotto=False
        self.wPieno=False
        self.wPortelloneAperto=False
        self.aAnomaliaGenerica=False
        self.aMotoreNastro=False
        self.aMancanzaConsenso=False
        self.aTemperaturaProdottoAlta=False
        self.aEmergenzaInserita=False
        self.aTemperaturaCpuElevata=False
        self.aAggraffatriceSpenta=False
        self.aNastroSpento=False
        self.contatorePezziTotale=0
        self.contatorePezziParziale=0
        self.contatorePezziParzialeBackup=0
        self.velocitaProduzionePezziMinuto=0
        self.temperaturaCpu=0

    def aggiornaStato(self,c):
        self.acceso=c[0]
        self.blocco=c[1]
        self.regime=c[2]
        self.wTermico=c[3]
        self.wAnomaliaNastro=c[4]
        self.wMancanzaProdotto=c[5]
        self.wPieno=c[6]
        self.wPortelloneAperto=c[7]
        self.aAnomaliaGenerica=c[8]
        self.aMotoreNastro=c[9]
        self.aMancanzaConsenso=c[10]
        self.aTemperaturaProdottoAlta=c[11]
        self.aEmergenzaInserita=c[12]
        self.aTemperaturaCpuElevata=c[13]
        self.aAggraffatriceSpenta=c[14]
        self.aNastroSpento=c[15]

    def controlloStato(self,c):
        if(self.acceso==c[0] and self.blocco==c[1] and self.regime==c[2] and self.wTermico==c[3] and self.wAnomaliaNastro==c[4] and self.wMancanzaProdotto==c[5] and self.wPieno==c[6] and self.wPortelloneAperto==c[7] and self.aAnomaliaGenerica==c[8] and self.aMotoreNastro==c[9] and self.aMancanzaConsenso==c[10] and self.aTemperaturaProdottoAlta==c[11] and self.aEmergenzaInserita==c[12] and self.aTemperaturaCpuElevata==c[13] and self.aAggraffatriceSpenta==c[14] and self.aNastroSpento==c[15]):
            return True
        else:
            return False

    def aggiornaContatori(self,h):
        self.contatorePezziTotale=h[0]
        self.contatorePezziParziale=h[1]
        self.contatorePezziParzialeBackup=h[2]
        self.velocitaProduzionePezziMinuto=h[3]
        self.temperaturaCpu=h[4]

    def controlloContatori(self,h):
        if(self.contatorePezziTotale==h[0] and self.contatorePezziParziale==h[1] and self.contatorePezziParzialeBackup==h[2] and self.velocitaProduzionePezziMinuto==h[3] and self.temperaturaCpu==h[4]):
            return True
        else:
            return False
