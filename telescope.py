import numscrypt as ns

class Telescope:
    def __init__ (self):
        pass
        
    def setParams (self,
    
    def project (self, projectableVec3D, rField, rScreen):
        '''Project scene upon screen
        
        Solar system radius of 1 m is mapped to image radius of 0.1 m.
        Eye distance from screen is 0.555 m, sun distance from screen is 5 m.
        Eye distance from sun (in origin) = 5.555 m = 10 * 0.555 m.
        So original of 1 m maps to image of 1 m / 10 = 0.1 m .
        0.1 m should be multiplied by 10 * rField to really fill half the screen.
        '''

        '''
        Initializing the required vectors
        '''

        zoomShift = 40 / zoomFactor	# 1..40

        dirVec0Plane = ns.array ((0, 1, 0))
        dirVec1Plane = ns.array ((0, 0, 1))
        
        '''
		supVecPlane = ns.array ((zoomShift / 2, 0, 0))
		supVecPlane = ns.array ((zoomShift / 6, 0, 0))
        '''
        supVecPlane =  ns.array ((6 / (6 * 6), 0, 0))

        '''
		supVecLine = ns.array (((1 + zoomShift) / 2, 0, 0))
		supVecLine = ns.array (((1 + zoomShift) / 6, 0, 0))
        '''
        supVecLine = ns.array (((1 + 6) / (6 * 6), 0, 0))

        '''
        Out through the backdoor if object behind eye
        '''
         
        if projectableVec3D [0] > supVecLine [0]:
            return None;
        }
    
        dirVecLine = projectableVec3D - supVecLine
 
        '''
        Line between eye and celestial body:    lineVec == supVecLine + a * dirVecLine
            
        Imag plane:                             planeVec == supVecPlane + b * dirVec0Plane + c * dirVec1Plane

        Intersection:                           lineVec == planeVec  ==>
        
                                                supVecLine + a * dirVecLine == supVecPlane + b * dirVec0Plane + c * dirVec1Plane
                                                
                                                                                     (dirVecLine.T)
                                                supVecPlane - supVecLine = (a, b, c) (-dirVec0Line.T)
                                                                                     (-dirVec1Line.T)
        '''
 
        '''
        Compute direction matrix
        '''
        
        dirMat = dirVecLine * ns.array ((1, 0, 0)) .T + dirVec0Plane * ns.array ((0, -1, 0)) .T  + dirVec1Plane * ns.array ((0, 0, -1)) .T + dirVecLine * ns.array ((1, 0, 0)) .T
        
        # Invert direction matrix
        
        double [][] invMat = new double [3][3];
        LinAlg.invert (invMat, dirMat);
        
        # Compute projection vector
        
        double [] supVecDif = new double [3];
        LinAlg.subtract (supVecDif, supVecPlane, supVecLine);
        
        double [] dirCoefVec = new double [3];
        LinAlg.mul (dirCoefVec, invMat, supVecDif);
        
        double [] termVecLine = new double [3];
        LinAlg.mul (termVecLine, dirCoefVec [0], dirVecLine);
        
        double [] projectedVec3D = new double [3];
        LinAlg.add (projectedVec3D, supVecLine, termVecLine);
        
        # rField in pixels / rScreen in m will map object with size of rScreen m exactly to rField pixels
        projectedVec2D = (
            (rField / (rScreen / 6d)) * projectedVec3D [1],
            (rField / (rScreen / 6d)) * projectedVec3D [2]
        )
        
        return true;
    }
            
        boolean map (double [] mappedVec2D, double [] mappableVec3D, double rField, double rScreen) {	
            double [] rotAngVec = new double [] {Math.PI / 180d * tilt, Math.PI/180d * course, 0d};
            
            double s, c;

            s = Math.sin (rotAngVec [1]);
            c = Math.cos (rotAngVec [1]);
                    
            double rotZCourseMat [][] = new double [][] {
                { c, -s, 0d},
                { s,  c, 0d},
                {0d, 0d, 1d}
            };

            s = Math.sin (rotAngVec [0]);
            c = Math.cos (rotAngVec [0]);
            
            double rotYTiltMat [][] = new double [][] {
                { c, 0d,  s},
                {0d, 1d, 0d},
                {-s, 0d,  c}
            };

            double rotationMat [][] = new double [3][3];
            double [] zoomedVec3D = new double [3];
            double [] rotatedVec = new double [3];
            
            LinAlg.mul (rotationMat, rotYTiltMat, rotZCourseMat);
            LinAlg.mul (zoomedVec3D, zoomFactor / 30d, mappableVec3D);
            LinAlg.mul (rotatedVec, rotationMat, zoomedVec3D);
            return project (mappedVec2D, rotatedVec, rField, rScreen);
        }
        
        boolean mapEyepiece (EyepieceImage eyepieceImage, Eyepiece eyepiece, double rField, double focLenObjective) {
            double magnif = focLenObjective / eyepiece.focLen;
            double angleUniverse = eyepiece.angle / magnif;
            eyepieceImage.rOnField = zoomFactor * rField * Math.sin ((Math.PI / 180d) * (angleUniverse / 2d));
            
            return eyepieceImage.rOnField < rField;
        }
    }
