if (sim_call_type==sim.syscb_init) then

    laserScannerHandle=sim.getObjectHandle("LaserScanner_2D")
    laserScannerObjectName=sim.getObjectName(laserScannerHandle)
    communicationTube=sim.tubeOpen(0,laserScannerObjectName..'_2D_SCANNER_DATA',1)
    motorLeft=sim.getObjectHandle("Pioneer_p3dx_leftMotor")
    motorRight=sim.getObjectHandle("Pioneer_p3dx_rightMotor")
    v0=10

end

if (sim_call_type==sim.syscb_cleanup) then

end

if (sim_call_type==sim.syscb_actuation) then

    data=sim.tubeRead(communicationTube)

    if (data) then

        laserDetectedPoints=sim.unpackFloatTable(data)

        vLeft=v0
        vRight=v0

        if laserDetectedPoints[2] > 1 then
            vLeft = vLeft - 0.5
            vRight = vRight + 0.5
        end

        if laserDetectedPoints[2] < 1 then
            vLeft = vLeft + 0.5
            vRight = vRight - 0.5
        end

        sim.setJointTargetVelocity(motorLeft,vLeft)
        sim.setJointTargetVelocity(motorRight,vRight)

    end

end
