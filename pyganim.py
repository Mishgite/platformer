
import pygame, time
PLAYING = 'playing'
PAUSED = 'paused'
STOPPED = 'stopped'

NORTHWEST = 'northwest'
NORTH = 'north'
NORTHEAST = 'northeast'
WEST = 'west'
CENTER = 'center'
EAST = 'east'
SOUTHWEST = 'southwest'
SOUTH = 'south'
SOUTHEAST = 'southeast'


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

    def reverse(self):
        # Reverses the order of the animations.
        self.elapsed = self._startTimes[-1] - self.elapsed
        self._images.reverse()
        self._transformedImages.reverse()
        self._durations.reverse()

    def getCopy(self):
        return self.getCopies(1)[0]

    def getCopies(self, numCopies=1):
        retval = []
        for i in range(numCopies):
            newAnim = PygAnimation('_copy', loop=self.loop)
            newAnim._images = self._images[:]
            newAnim._transformedImages = self._transformedImages[:]
            newAnim._durations = self._durations[:]
            newAnim._startTimes = self._startTimes[:]
            newAnim.numFrames = self.numFrames
            retval.append(newAnim)
        return retval

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

    def getCurrentFrame(self):
        return self.getFrame(self.currentFrameNum)

    def clearTransforms(self):
        self._transformedImages = []

    def makeTransformsPermanent(self):
        self._images = [pygame.Surface(surfObj.get_size(), 0, surfObj) for surfObj in self._transformedImages]
        for i in range(len(self._transformedImages)):
            self._images[i].blit(self._transformedImages[i], (0,0))

    def blitFrameNum(self, frameNum, destSurface, dest):
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        destSurface.blit(self.getFrame(frameNum), dest)

    def blitFrameAtTime(self, elapsed, destSurface, dest):
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        frameNum = findStartTime(self._startTimes, elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)

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

    def togglePause(self):
        if self._state == PLAYING:
            if self.isFinished():
                self.play()
            else:
                self.pause()
        elif self._state in (PAUSED, STOPPED):
            self.play()

    def areFramesSameSize(self):
        width, height = self.getFrame(0).get_size()
        for i in range(len(self._images)):
            if self.getFrame(i).get_size() != (width, height):
                return False
        return True

    def getMaxSize(self):
        frameWidths = []
        frameHeights = []
        for i in range(len(self._images)):
            frameWidth, frameHeight = self._images[i].get_size()
            frameWidths.append(frameWidth)
            frameHeights.append(frameHeight)
        maxWidth = max(frameWidths)
        maxHeight = max(frameHeights)

        return (maxWidth, maxHeight)

    def getRect(self):
        maxWidth, maxHeight = self.getMaxSize()
        return pygame.Rect(0, 0, maxWidth, maxHeight)

    def anchor(self, anchorPoint=NORTHWEST):
        if self.areFramesSameSize():
            return
        self.clearTransforms()
        maxWidth, maxHeight = self.getMaxSize()
        halfMaxWidth = int(maxWidth / 2)
        halfMaxHeight = int(maxHeight / 2)

        for i in range(len(self._images)):
            newSurf = pygame.Surface((maxWidth, maxHeight))
            newSurf = newSurf.convert_alpha()
            newSurf.fill((0,0,0,0))

            frameWidth, frameHeight = self._images[i].get_size()
            halfFrameWidth = int(frameWidth / 2)
            halfFrameHeight = int(frameHeight / 2)

            if anchorPoint == NORTHWEST:
                newSurf.blit(self._images[i], (0, 0))
            elif anchorPoint == NORTH:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, 0))
            elif anchorPoint == NORTHEAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, 0))
            elif anchorPoint == WEST:
                newSurf.blit(self._images[i], (0, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == CENTER:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == EAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == SOUTHWEST:
                newSurf.blit(self._images[i], (0, maxHeight - frameHeight))
            elif anchorPoint == SOUTH:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, maxHeight - frameHeight))
            elif anchorPoint == SOUTHEAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, maxHeight - frameHeight))
            self._images[i] = newSurf

    def nextFrame(self, jump=1):
        self.currentFrameNum += int(jump)

    def prevFrame(self, jump=1):
        self.currentFrameNum -= int(jump)

    def rewind(self, seconds=None):
        if seconds is None:
            self.elapsed = 0.0
        else:
            self.elapsed -= seconds

    def fastForward(self, seconds=None):
        if seconds is None:
            self.elapsed = self._startTimes[-1] - 0.00002
        else:
            self.elapsed += seconds

    def _makeTransformedSurfacesIfNeeded(self):
        if self._transformedImages == []:
            self._transformedImages = [surf.copy() for surf in self._images]

    def flip(self, xbool, ybool):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.flip(self.getFrame(i), xbool, ybool)

    def scale(self, width_height):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.scale(self.getFrame(i), width_height)

    def rotate(self, angle):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.rotate(self.getFrame(i), angle)

    def rotozoom(self, angle, scale):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.rotozoom(self.getFrame(i), angle, scale)

    def scale2x(self):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.scale2x(self.getFrame(i))

    def smoothscale(self, width_height):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.smoothscale(self.getFrame(i), width_height)

    def _surfaceMethodWrapper(self, wrappedMethodName, *args, **kwargs):
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            methodToCall = getattr(self._transformedImages[i], wrappedMethodName)
            methodToCall(*args, **kwargs)

    def convert(self, *args, **kwargs):
        self._surfaceMethodWrapper('convert', *args, **kwargs)


    def convert_alpha(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.convert_alpha
        self._surfaceMethodWrapper('convert_alpha', *args, **kwargs)


    def set_alpha(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.set_alpha
        self._surfaceMethodWrapper('set_alpha', *args, **kwargs)


    def scroll(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.scroll
        self._surfaceMethodWrapper('scroll', *args, **kwargs)


    def set_clip(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.set_clip
        self._surfaceMethodWrapper('set_clip', *args, **kwargs)


    def set_colorkey(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.set_colorkey
        self._surfaceMethodWrapper('set_colorkey', *args, **kwargs)


    def lock(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.unlock
        self._surfaceMethodWrapper('lock', *args, **kwargs)


    def unlock(self, *args, **kwargs):
        # See http://pygame.org/docs/ref/surface.html#Surface.lock
        self._surfaceMethodWrapper('unlock', *args, **kwargs)

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
        elapsed += 0.00001 # done to compensate for rounding errors
        return elapsed

    elapsed = property(_propGetElapsed, _propSetElapsed)

    def _propGetCurrentFrameNum(self):
        return findStartTime(self._startTimes, self.elapsed)


    def _propSetCurrentFrameNum(self, frameNum):
        # Change the elapsed time to the beginning of a specific frame.
        if self.loop:
            frameNum = frameNum % len(self._images)
        else:
            frameNum = getInBetweenValue(0, frameNum, len(self._images)-1)
        self.elapsed = self._startTimes[frameNum]

    currentFrameNum = property(_propGetCurrentFrameNum, _propSetCurrentFrameNum)



class PygConductor(object):
    def __init__(self, *animations):
        assert len(animations) > 0, 'at least one PygAnimation object is required'

        self._animations = []
        self.add(*animations)


    def add(self, *animations):
        if type(animations[0]) == dict:
            for k in animations[0].keys():
                self._animations.append(animations[0][k])
        elif type(animations[0]) in (tuple, list):
            for i in range(len(animations[0])):
                self._animations.append(animations[0][i])
        else:
            for i in range(len(animations)):
                self._animations.append(animations[i])

    def _propGetAnimations(self):
        return self._animations

    def _propSetAnimations(self, val):
        self._animations = val

    animations = property(_propGetAnimations, _propSetAnimations)

    def play(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        for animObj in self._animations:
            animObj.play(startTime)

    def pause(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        for animObj in self._animations:
            animObj.pause(startTime)

    def stop(self):
        for animObj in self._animations:
            animObj.stop()

    def reverse(self):
        for animObj in self._animations:
            animObj.reverse()

    def clearTransforms(self):
        for animObj in self._animations:
            animObj.clearTransforms()

    def makeTransformsPermanent(self):
        for animObj in self._animations:
            animObj.makeTransformsPermanent()

    def togglePause(self):
        for animObj in self._animations:
            animObj.togglePause()

    def nextFrame(self, jump=1):
        for animObj in self._animations:
            animObj.nextFrame(jump)

    def prevFrame(self, jump=1):
        for animObj in self._animations:
            animObj.prevFrame(jump)

    def rewind(self, seconds=None):
        for animObj in self._animations:
            animObj.rewind(seconds)

    def fastForward(self, seconds=None):
        for animObj in self._animations:
            animObj.fastForward(seconds)

    def flip(self, xbool, ybool):
        for animObj in self._animations:
            animObj.flip(xbool, ybool)

    def scale(self, width_height):
        for animObj in self._animations:
            animObj.scale(width_height)

    def rotate(self, angle):
        for animObj in self._animations:
            animObj.rotate(angle)

    def rotozoom(self, angle, scale):
        for animObj in self._animations:
            animObj.rotozoom(angle, scale)

    def scale2x(self):
        for animObj in self._animations:
            animObj.scale2x()

    def smoothscale(self, width_height):
        for animObj in self._animations:
            animObj.smoothscale(width_height)

    def convert(self):
        for animObj in self._animations:
            animObj.convert()

    def convert_alpha(self):
        for animObj in self._animations:
            animObj.convert_alpha()

    def set_alpha(self, *args, **kwargs):
        for animObj in self._animations:
            animObj.set_alpha(*args, **kwargs)

    def scroll(self, dx=0, dy=0):
        for animObj in self._animations:
            animObj.scroll(dx, dy)

    def set_clip(self, *args, **kwargs):
        for animObj in self._animations:
            animObj.set_clip(*args, **kwargs)

    def set_colorkey(self, *args, **kwargs):
        for animObj in self._animations:
            animObj.set_colorkey(*args, **kwargs)

    def lock(self):
        for animObj in self._animations:
            animObj.lock()

    def unlock(self):
        for animObj in self._animations:
            animObj.unlock()

def getInBetweenValue(lowerBound, value, upperBound):
    if value < lowerBound:
        return lowerBound
    elif value > upperBound:
        return upperBound
    return value


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
