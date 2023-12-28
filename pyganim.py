import pygame, time
PLAYING, PAUSED, STOPPED, NORTHWEST, NORTH, NORTHEAST, WEST, CENTER, EAST, SOUTHWEST, SOUTH, SOUTHEAST = 'playing',\
    'paused', 'stopped', 'northwest', 'north', 'northeast', 'west', 'center', 'east', 'southwest', 'south', 'southeast'


class PygAnimation(object):
    def __init__(self, frames, loop=True):
        self._images = []
        self._durations = []
        self._startTimes = None
        self._transformedImages = []
        self._state = STOPPED
        self._loop = loop
        self._rate = 1.0
        self._visibility = True
        self._playingStartTime = 0
        self._pausedStartTime = 0
        if frames != '_copy':
            self.numFrames = len(frames)
            assert self.numFrames > 0, 'Must contain at least one frame.'
            for i in range(self.numFrames):
                frame = frames[i]
                assert type(frame) in (list, tuple) and len(frame) == 2, 'Frame %s has incorrect format.' % (i)
                assert type(frame[0]) in (str, pygame.Surface), 'Frame %s image must be a string filename or a pygame.Surface' % (i)
                assert frame[1] > 0, 'Frame %s duration must be greater than zero.' % (i)
                if type(frame[0]) == str:
                    frame = (pygame.image.load(frame[0]), frame[1])
                self._images.append(frame[0])
                self._durations.append(frame[1])
            self._startTimes = self._getStartTimes()

    def _getStartTimes(self):
        startTimes = [0]
        for i in range(self.numFrames):
            startTimes.append(startTimes[-1] + self._durations[i])
        return startTimes

    def blit(self, destSurface, dest):
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        frameNum = findStartTime(self._startTimes, self.elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)

    def getFrame(self, frameNum):
        if self._transformedImages == []:
            return self._images[frameNum]
        else:
            return self._transformedImages[frameNum]

    def isFinished(self):
        return not self.loop and self.elapsed >= self._startTimes[-1]

    def play(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        if self._state == PLAYING:
            if self.isFinished():
                self._playingStartTime = startTime
        elif self._state == STOPPED:
            self._playingStartTime = startTime
        elif self._state == PAUSED:
            self._playingStartTime = startTime - (self._pausedStartTime - self._playingStartTime)
        self._state = PLAYING

    def pause(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        if self._state == PAUSED:
            return # do nothing
        elif self._state == PLAYING:
            self._pausedStartTime = startTime
        elif self._state == STOPPED:
            rightNow = time.time()
            self._playingStartTime = rightNow
            self._pausedStartTime = rightNow
        self._state = PAUSED

    def stop(self):
        if self._state == STOPPED:
            return # do nothing
        self._state = STOPPED

    def nextFrame(self, jump=1):
        self.currentFrameNum += int(jump)

    def _propGetRate(self):
        return self._rate

    def _propSetRate(self, rate):
        rate = float(rate)
        if rate < 0:
            raise ValueError('rate must be greater than 0.')
        self._rate = rate
    rate = property(_propGetRate, _propSetRate)

    def _propGetLoop(self):
        return self._loop

    def _propSetLoop(self, loop):
        if self.state == PLAYING and self._loop and not loop:
            self._playingStartTime = time.time() - self.elapsed
        self._loop = bool(loop)
    loop = property(_propGetLoop, _propSetLoop)

    def _propGetState(self):
        if self.isFinished():
            self._state = STOPPED
        return self._state

    def _propSetState(self, state):
        if state not in (PLAYING, PAUSED, STOPPED):
            raise ValueError('state must be one of pyganim.PLAYING, pyganim.PAUSED, or pyganim.STOPPED')
        if state == PLAYING:
            self.play()
        elif state == PAUSED:
            self.pause()
        elif state == STOPPED:
            self.stop()
    state = property(_propGetState, _propSetState)

    def _propGetVisibility(self):
        return self._visibility
    def _propSetVisibility(self, visibility):
        self._visibility = bool(visibility)
    visibility = property(_propGetVisibility, _propSetVisibility)

    def _propSetElapsed(self, elapsed):
        elapsed += 0.00001
        if self._loop:
            elapsed = elapsed % self._startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self._startTimes[-1])

        rightNow = time.time()
        self._playingStartTime = rightNow - (elapsed * self.rate)

        if self.state in (PAUSED, STOPPED):
            self.state = PAUSED
            self._pausedStartTime = rightNow

    def _propGetElapsed(self):
        if self._state == STOPPED:
            return 0
        if self._state == PLAYING:
            elapsed = (time.time() - self._playingStartTime) * self.rate
        elif self._state == PAUSED:
            elapsed = (self._pausedStartTime - self._playingStartTime) * self.rate
        if self._loop:
            elapsed = elapsed % self._startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self._startTimes[-1])
        elapsed += 0.00001
        return elapsed
    elapsed = property(_propGetElapsed, _propSetElapsed)

    def _propGetCurrentFrameNum(self):
        return findStartTime(self._startTimes, self.elapsed)

    def _propSetCurrentFrameNum(self, frameNum):
        if self.loop:
            frameNum = frameNum % len(self._images)
        else:
            frameNum = getInBetweenValue(0, frameNum, len(self._images)-1)
        self.elapsed = self._startTimes[frameNum]
    currentFrameNum = property(_propGetCurrentFrameNum, _propSetCurrentFrameNum)

def findStartTime(startTimes, target):
    assert startTimes[0] == 0
    lb = 0
    ub = len(startTimes) - 1
    if len(startTimes) == 0:
        return 0
    if target >= startTimes[-1]:
        return ub - 1
    while True:
        i = int((ub - lb) / 2) + lb
        if startTimes[i] == target or (startTimes[i] < target and startTimes[i+1] > target):
            if i == len(startTimes):
                return i - 1
            else:
                return i
        if startTimes[i] < target:
            lb = i
        elif startTimes[i] > target:
            ub = i