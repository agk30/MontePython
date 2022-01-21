import configparser
import math

class LoadInputs:
    def __init__(self):
        
        inputs = configparser.ConfigParser()

        inputs.read("../inputs.cfg")

        self.skimPos = float(inputs['experimental']['skimPos'])
        self.valvePos = float(inputs['experimental']['valvePos'])
        self.colPos = float(inputs['experimental']['colPos'])
        self.skimRad = float(inputs['experimental']['skimRad'])
        self.valveRad = float(inputs['experimental']['valveRad'])
        self.colRad = float(inputs['experimental']['colRad'])
        self.sheetCentre = float(inputs['experimental']['sheetCentre'])
        self.halfSheetHeight = float(inputs['experimental']['halfSheetHeight'])
        self.sheetWidth = float(inputs['experimental']['sheetWidth'])
        self.pulseLength = float(inputs['experimental']['pulseLength'])
        self.surface_z = float(inputs['experimental']['surface_z'])

        #Inputs regarding the imaging process
        self.pxMmRatio = float(inputs['imaging']['pxMmRatio'])
        self.probeStart = float(inputs['imaging']['probeStart'])
        self.probeEnd = float(inputs['imaging']['probeEnd'])
        self.tStep = float(inputs['imaging']['tStep'])
        self.gaussBlurDev = float(inputs['imaging']['gaussBlurDev'])
        self.ksize = int(inputs['imaging']['ksize'])
        self.polyOrder = int(inputs['imaging']['polyOrder'])
        self.scattering = bool(inputs['imaging']['scattering'])
        self.ingoingBeam = bool(inputs['imaging']['ingoingBeam'])
        self.writeImages = bool(inputs['imaging']['writeImages'])
        self.scatterIntensity = float(inputs['imaging']['scatterIntensity'])
        self.fLifeTime = float(inputs['imaging']['fLifeTime'])
        self.captureGateOpen = float(inputs['imaging']['captureGateOpen'])
        self.captureGateClose = float(inputs['imaging']['captureGateClose'])

        #Iputs for mathematical calculations
        self.xPx = int(inputs['math parameters']['xPx'])
        self.zPx = int(inputs['math parameters']['zPx'])
        self.incidenceAngle = math.radians(int(inputs['math parameters']['incidenceAngle']))
        self.cosinePowerTD = int(inputs['math parameters']['cosinePowerTD'])
        self.cosinePowerIS = int(inputs['math parameters']['cosinePowerIS'])
        self.x0 = float(inputs['math parameters']['x0'])
        self.aMax = float(inputs['math parameters']['aMax'])
        self.aMin = float(inputs['math parameters']['aMin'])
        self.h = float(inputs['math parameters']['h'])
        self.s = float(inputs['math parameters']['s'])
        self.dist = float(inputs['math parameters']['dist'])
        self.mass = float(inputs['math parameters']['mass'])
        self.massMol = float(inputs['math parameters']['massMol'])
        self.energyLoss = float(inputs['math parameters']['energyLoss'])
        self.surfaceMass = float(inputs['math parameters']['surfaceMass'])
        self.exitAngle = math.radians(float(inputs['math parameters']['exitAngle']))
        self.temp = float(inputs['math parameters']['temp'])
        self.ncyc = int(inputs['math parameters']['ncyc'])
        self.maxSpeed = float(inputs['math parameters']['maxSpeed'])
        self.ISscatterFraction = float(inputs['math parameters']['ISscatterFraction'])

        self.gaussMeans = []
        self.gaussDevs = []
        self.gaussWeights = []

        for item in inputs['math parameters']['gaussMeans'].split():
            self.gaussMeans.append(float(item))

        for item in inputs['math parameters']['gaussDevs'].split():
            self.gaussDevs.append(float(item))

        for item in inputs['math parameters']['gaussWeights'].split():
            self.gaussWeights.append(float(item))

        self.gaussDist = float(inputs['math parameters']['gaussDist'])
        self.timeOffset = float(inputs['math parameters']['timeOffset'])

        self.imagePath = str(inputs['file paths']['imagePath'])
        self.matrixPath = str(inputs['file paths']['matrixPath'])
        self.ifPath = str(inputs['file paths']['ifPath'])