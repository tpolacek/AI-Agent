# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageFilter
import math, operator


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        # threshold for what is considered a match with blur and downscaling
        self.threshold = 76.0
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):

        # prepare images for use
        img_dict = self.prep_images(problem)

        # Need to solve a 2x2 problem
        if problem.problemType == '2x2':

            # prepare answers for comparison
            ans_dict = {'1': img_dict['1'], '2': img_dict['2'], '3': img_dict['3'],
                        '4': img_dict['4'], '5': img_dict['5'], '6': img_dict['6']}

            # group figures into primary or secondary comparison
            orient = self.test_2x2_visuals(img_dict)
            (orientation1, figOne, figTwo, figThree), (orientation2, aFigOne, aFigTwo, aFigThree) = \
                self.group_2x2_visuals(img_dict, orient)

            primary_figs = [figOne, figTwo, figThree]
            secondary_figs = [aFigOne, aFigTwo, aFigThree]

            # send problems to solver method
            solution1, method1 = self.hv_visual_solver(primary_figs, ans_dict)
            solution2, method2 = self.hv_visual_solver(secondary_figs, ans_dict)

            common_solutions = [val for val in solution1 if val in solution2]

            # if there is a single common solution, return that as the answer
            if len(common_solutions) == 1:
                return int(common_solutions[0])
            else:
                # find the solution with the lowest comparison score
                best = 999
                winner1 = []
                winner2 = []

                for aKey, aVal in solution1.iteritems():
                    if aVal < best:
                        best = aVal
                        winner1 = [aKey, aVal]

                best = 999
                for aKey, aVal in solution2.iteritems():
                    if aVal < best:
                        best = aVal
                        winner2 = [aKey, aVal]

                if winner1[1] < winner2[1]:
                    return int(winner1[0])
                else:
                    return int(winner2[0])

        # Need to solve a 3x3 problem
        else:
            # prepare answers for comparison
            ans_dict = {'1': img_dict['1'], '2': img_dict['2'], '3': img_dict['3'], '4': img_dict['4'],
                        '5': img_dict['5'], '6': img_dict['6'], '7':img_dict['7'], '8': img_dict['8']}

            # group figures into primary and secondary comparisons
            orient = self.test_3x3_visuals(img_dict)
            if orient != 'Diagonal':
                (orientation1, figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight), \
                (orientation2, aFigOne, aFigTwo, aFigThree, aFigFour, aFigFive, aFigSix, aFigSeven, aFigEight) = \
                    self.group_3x3_visuals(img_dict, orient)

                primary_figs = [figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight]
                secondary_figs = [aFigOne, aFigTwo, aFigThree, aFigFour, aFigFive, aFigSix, aFigSeven, aFigEight]

                # send problems to solver method
                solution1, method1 = self.hv_visual_solver(primary_figs, ans_dict)
                solution2, method2 = self.hv_visual_solver(secondary_figs, ans_dict)

                all_solutions = list(set(solution1) | set(solution2))
                common_solutions = [val for val in solution1 if val in solution2]

                # if there is a single common solution, return that as the answer
                if len(common_solutions) == 1:
                    return int(common_solutions[0])

                # begin process of breaking ties
                # first look at if the method was a growth factor and there were more than 3 common solutions,
                # else other tiebreakers can handle the rest
                if method1 == 'growth' and method2 == 'growth':
                    if len(common_solutions) > 2:

                        # rule out perfect matches, as it was already determined that was not the case
                        removals = []
                        for aKey, aVal in solution1.iteritems():
                            if aVal < 50.0:
                                removals.append(aKey)

                        for j in removals:
                            solution1.pop(j, None)

                        winner = []
                        best = 999.9
                        for aKey, aVal in solution1.iteritems():
                            if aVal < best:
                                best = aVal
                                winner = [aKey, aVal]

                        return int(winner[0])

                # next check by cropping image to just look at the center horizontal strip of the figures
                solution = {}
                if len(common_solutions) == 2:
                    for guess in common_solutions:
                        cropped_guess = ans_dict[guess].crop((0,15,50,35))

                        if guess in solution1:
                            comp = figSeven.crop((0,15,50,35))
                        else:
                            comp = aFigSeven.crop((0,15,50,35))

                        solution[guess] = self.compare_images(cropped_guess, comp)

                else:
                    for guess in all_solutions:
                        cropped_guess = ans_dict[guess].crop((0,15,50,35))

                        if guess in solution1:
                            comp = figSeven.crop((0,15,50,35))
                        else:
                            comp = aFigSeven.crop((0,15,50,35))

                        solution[guess] = self.compare_images(cropped_guess, comp)

                # if difference between tiebreaker is too small to be significant, go with the original best answer
                if len(all_solutions) == 2:
                    ks = solution.keys()
                    difference = abs(solution[ks[0]] - solution[ks[1]])
                    if difference < 10:
                        allsols = solution1.copy()
                        allsols.update(solution2)
                        for k, v in allsols.iteritems():
                            if v < 10.0:
                                return int(k)

                # disregard any perfect matches found in the center strip,
                # as it was already established there is not a perfect match
                removals = []
                for aKey, aVal in solution.iteritems():
                    if aVal == 0.0:
                        removals.append(aKey)

                for j in removals:
                    solution.pop(j, None)


                # check for the black pixel count decreasing from image to image,
                # basically is the image getting smaller in the end portion of each row/column

                # first get a black pixel count for each figure in the primary figures list and store that info
                try:
                    bcountF = {}
                    cnt = 1
                    for k in primary_figs:
                        b, w = k.getcolors()
                        bcountF[str(cnt)] = b
                        cnt += 1

                    # do same for answers
                    ks = solution.keys()
                    bcountA = {}
                    for j in ks:
                        b, w = ans_dict[j].getcolors()
                        bcountA[j] = b

                # if there is only 1 color in the figure, skip the problem
                except ValueError:
                    return -1

                # then check if the 3rd element in each row/col is proportionally smaller than the 1st and 2nd
                s1 = abs(bcountF['1'][0] - bcountF['2'][0])
                s2 = abs(bcountF['4'][0] - bcountF['5'][0])
                s3 = abs(bcountF['7'][0] - bcountF['8'][0])
                c = bcountF['1'][0] - bcountF['3'][0]
                f = bcountF['4'][0] - bcountF['6'][0]
                if s1 < 20 and s2 < 20 and s3 < 20 and c > 90 and f > 90:
                    for aKey, aVal in solution.iteritems():
                        i = bcountF['7'][0] - bcountA[aKey][0]
                        if i > 90:
                            return int(aKey)

                # if there are still too many solutions, skip the problem, otherwise take the
                # solution with the best comparison score as determined in the tiebreaker
                if len(solution.keys()) > 7:
                    return -1
                else:
                    best = 999.9
                    for k, v in solution.iteritems():
                        if v < best:
                            best = v
                            winner = k

                    return int(winner)

            else:
                orientation, figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight = \
                    self.group_3x3_visuals(img_dict, orient)

                primary_figs = [figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight]

                # send problem to solver method
                solution, method = self.d_visual_solver(primary_figs, ans_dict)

                # begin process of breaking ties betweEn solutions
                if len(solution.keys()) > 1:

                    # start by ruling out perfect matches if the first 2 figures aren't matches
                    if method != 'matching':
                        removals = []
                        for aKey, aVal in solution.iteritems():
                            diff = self.compare_images(figTwo, ans_dict[aKey])
                            if diff <= 40.0:
                                removals.append(aKey)

                        for j in removals:
                            solution.pop(j, None)

                    if len(solution.keys()) == 1:
                        return int(solution.keys()[0])

                    # next look at relationship between the potential answer
                    # and the reverse diagonal relationship (compare answer to B and D)
                    if method != 'matching':
                        best = 999.9
                        winner = None
                        for guess in solution.keys():
                            Bcomp = self.compare_images(img_dict['B'], ans_dict[guess])
                            Dcomp = self.compare_images(img_dict['D'], ans_dict[guess])
                            # rule out any perfect matches, since that is not the method used before
                            if Bcomp > 45.0 and Dcomp > 45.0:
                                diff = Bcomp + Dcomp
                                if diff < best:
                                    winner = guess
                                    best = diff

                        if winner is not None:
                            return int(winner)

                    # finally, if no winner found yet, pick the solution with
                    # best difference score as found earlier
                    best = 999.9
                    for k, v in solution.iteritems():
                        if v < best:
                            best = v
                            winner = k

                    return int(winner)

            return int(solution.keys()[0])


    # Method to prepare image files for use in the agent
    def prep_images(self, problem):

        # dictionary to store the loaded image files in
        img_dict = {}

        # open, convert to black and white, and store
        for key in problem.figures:
            fname = problem.figures[key].visualFilename
            image = Image.open(fname)
            image = image.filter(ImageFilter.GaussianBlur)
            image = image.resize((50, 50))
            image = image.convert('1')
            img_dict[key] = image

        return img_dict

    # Method for comparing how similar visual images are
    def compare_images(self, img1, img2):

        "Calculate the root-mean-square difference between two images"
        # source code --> http://effbot.org/zone/pil-comparing-images.htm

        rotations = [350, 352, 354, 356, 358, 359, 0, 1, 2, 4, 6, 8, 10]
        differences = []

        # slight rotations for each image to find the best fit within a few pixels either way
        for deg in rotations:

            img2r = img2.rotate(deg)

            h = ImageChops.difference(img1, img2r).histogram()

            rms = math.sqrt(reduce(operator.add,
            map(lambda h, i: h*(i**2), h, range(256))
            ) / (float(img1.size[0]) * img1.size[1]))

            differences.append(rms)

        # calculate rms
        return min(differences)

    # Methods for finding the primary/secondary comparisons
    def test_2x2_visuals(self, imgs):

        horizontal = self.compare_images(imgs['A'], imgs['B'])
        vertical = self.compare_images(imgs['A'], imgs['B'])

        if horizontal < vertical:
            return 'Horizontal'
        else:
            return 'Vertical'

    def test_3x3_visuals(self, imgs):

        horizontal = 0
        vertical = 0
        diagonal = 0

        horizontal += self.compare_images(imgs['A'], imgs['B'])
        horizontal += self.compare_images(imgs['B'], imgs['C'])

        vertical += self.compare_images(imgs['A'], imgs['D'])
        vertical += self.compare_images(imgs['D'], imgs['G'])

        diagonal += self.compare_images(imgs['A'], imgs['E'])
        diagonal += self.compare_images(imgs['B'], imgs['F'])

        count_lst = [vertical, diagonal, horizontal]
        min_score = min(count_lst)

        if horizontal == min_score:
            return 'Horizontal'
        elif vertical == min_score:
            return 'Vertical'
        else:
            return 'Diagonal'


    # Methods to group the figures into the correct order for comparisons
    def group_2x2_visuals(self, imgs, orientation):
        if orientation == 'Horizontal':
            return ('Horizontal', imgs['A'], imgs['B'], imgs['C']), ('Vertical', imgs['A'], imgs['C'], imgs['B'])
        else:
            return ('Vertical', imgs['A'], imgs['C'], imgs['B']), ('Horizontal', imgs['A'], imgs['B'], imgs['C'])

    def group_3x3_visuals(self, imgs, orientation):

        if orientation == 'Diagonal':
            return 'Diagonal', imgs['A'], imgs['E'], imgs['B'], imgs['F'], \
                   imgs['D'], imgs['H'], imgs['C'], imgs['G']

        elif orientation == 'Horizontal':
            return ('Horizontal', imgs['A'], imgs['B'], imgs['C'], imgs['D'],
                    imgs['E'], imgs['F'], imgs['G'], imgs['H']), \
                   ('Vertical', imgs['A'], imgs['D'], imgs['G'], imgs['B'],
                    imgs['E'], imgs['H'], imgs['C'], imgs['F'])

        else:
            return ('Vertical', imgs['A'], imgs['D'], imgs['G'], imgs['B'],
                    imgs['E'], imgs['H'], imgs['C'], imgs['F']), \
                    ('Horizontal', imgs['A'], imgs['B'], imgs['C'], imgs['D'],
                    imgs['E'], imgs['F'], imgs['G'], imgs['H'])


    # Methods to solve visual problems after grouping
    def d_visual_solver(self, figs, ans_dict):

        solutions = {}

        # Diagonal comparisons to go against
        f1_f2 = self.compare_images(figs[0], figs[1])

        # test for matching, under 50 is a match
        meth = 'matching'
        if f1_f2 < 50.0:
            for aKey, aVal in ans_dict.iteritems():
                diff = self.compare_images(figs[1], ans_dict[aKey])
                if  diff < 50.0:
                    solutions[aKey] = diff

        if solutions:
            return solutions, meth

        # test for rotations, under 80 is a match
        meth = 'rotations'
        rotations = [45, 90, 135, 180, 225, 270, 315]
        for degs in rotations:
            f1_f2 = self.compare_images(figs[0].rotate(degs), figs[1])

            if f1_f2 < self.threshold:
                for aKey, aVal in ans_dict.iteritems():
                    diff = self.compare_images(figs[1].rotate(degs), ans_dict[aKey])
                    if  diff < self.threshold:
                        solutions[aKey] = diff

        if solutions:
            return solutions, meth

        # test for reflections, under 80 is a match
        meth = 'reflections'
        transforms = [Image.FLIP_TOP_BOTTOM, Image.FLIP_LEFT_RIGHT]
        for flip in transforms:
            f1_f2 = self.compare_images(figs[0].transpose(flip), figs[1])

            if f1_f2 < self.threshold:
                for aKey, aVal in ans_dict.iteritems():
                    diff = self.compare_images(figs[1].transpose(flip), ans_dict[aKey])
                    if diff < self.threshold:
                        solutions[aKey] = diff

        if solutions:
            return solutions, meth

        # if no match yet, go by raw pixel data
        meth = 'raw comp'
        best_distance = 9999.9

        set1_score = self.compare_images(figs[0], figs[1])
        set2_score = self.compare_images(figs[2], figs[3])
        set3_score = self.compare_images(figs[4], figs[5])

        for aKey, aVal in ans_dict.iteritems():
            set4_score = self.compare_images(figs[1], ans_dict[aKey])

            cur_distance = (abs(set1_score - set4_score) + abs(set2_score - set4_score) + abs(set3_score - set4_score))

            if cur_distance <= best_distance:
                best_distance = cur_distance
                winner = [aKey, best_distance]

        solutions[winner[0]] = winner[1]
        return solutions, meth

    def hv_visual_solver(self, figs, ans_dict):
        solutions = {}

        # first check for matching images
        solutions = self.test_matching(figs, ans_dict)

        if solutions:
            return solutions, 'matching'

        # next check for rotations
        solutions = self.test_rotations(figs, ans_dict)

        if solutions:
            return solutions, 'rotations'

        # next check for reflections
        solutions = self.test_reflections(figs, ans_dict)

        if solutions:
            return solutions, 'reflections'

        # next check for growth in the figure
        solutions = self.test_growth(figs, ans_dict)

        if solutions:
            return solutions, 'growth'

        # compare raw image and pixel data if no match found yet
        solutions = self.raw_comparison(figs, ans_dict)

        if solutions:
            return solutions, 'raw'

        # if nothing was found yet, skip the problem, shouldn't happen
        return -1


    # Helper methods for the visual solver
    def test_matching(self, figs, ans_dict):

        # anything under 50 will be a match
        solutions = {}

        if len(figs) == 3:
            if self.compare_images(figs[0], figs[1]) < 50.0:
                for aKey, aVal in ans_dict.iteritems():
                    diff = self.compare_images(figs[2], ans_dict[aKey])
                    if diff < 50.0:
                        solutions[aKey] = diff

        else:
            f1_f2 = self.compare_images(figs[0], figs[1])
            f2_f3 = self.compare_images(figs[1], figs[2])

            f4_f5 = self.compare_images(figs[3], figs[4])
            f5_f6 = self.compare_images(figs[4], figs[5])

            f7_f8 = self.compare_images(figs[6], figs[7])

            images = [f1_f2, f2_f3, f4_f5, f5_f6, f7_f8]

            if max(images) < 50.0:
                for aKey, aVal in ans_dict.iteritems():
                    diff = self.compare_images(figs[7], ans_dict[aKey])
                    if  diff < 50.0:
                        solutions[aKey] = diff

        return solutions

    def test_rotations(self, figs, ans_dict):
        # anything under 80 will be a match
        solutions = {}
        rotations = [45, 90, 135, 180, 225, 270, 315]

        if len(figs) == 3:
            for deg in rotations:
                if self.compare_images(figs[0].rotate(deg), figs[1]) < self.threshold:
                    for aKey, aVal in ans_dict.iteritems():
                        diff = self.compare_images(figs[2].rotate(deg), ans_dict[aKey])
                        if diff < self.threshold:
                            solutions[aKey] = diff

        else:
            for deg in rotations:
                f1_f2 = self.compare_images(figs[0].rotate(deg), figs[1])
                f2_f3 = self.compare_images(figs[1].rotate(deg), figs[2])

                f4_f5 = self.compare_images(figs[3].rotate(deg), figs[4])
                f5_f6 = self.compare_images(figs[4].rotate(deg), figs[5])

                f7_f8 = self.compare_images(figs[6].rotate(deg), figs[7])

                images = [f1_f2, f2_f3, f4_f5, f5_f6, f7_f8]

                if max(images) < self.threshold:
                    for aKey, aVal in ans_dict.iteritems():
                        diff = self.compare_images(figs[7].rotate(deg), ans_dict[aKey])
                        if  diff < self.threshold:
                            solutions[aKey] = diff

        return solutions

    def test_reflections(self, figs, ans_dict):
        # anything under 80 will be a match
        solutions = {}
        transforms = [Image.FLIP_TOP_BOTTOM, Image.FLIP_LEFT_RIGHT]

        if len(figs) == 3:
            for flip in transforms:
                if self.compare_images(figs[0].transpose(flip), figs[1]) < self.threshold:
                    for aKey, aVal in ans_dict.iteritems():
                        diff = self.compare_images(figs[2].transpose(flip), ans_dict[aKey])
                        if diff < self.threshold:
                            solutions[aKey] = diff

        else:
            for flip in transforms:
                f1_f2 = self.compare_images(figs[0].transpose(flip), figs[1])
                f2_f3 = self.compare_images(figs[1].transpose(flip), figs[2])

                f4_f5 = self.compare_images(figs[3].transpose(flip), figs[4])
                f5_f6 = self.compare_images(figs[4].transpose(flip), figs[5])

                f7_f8 = self.compare_images(figs[6].transpose(flip), figs[7])

                images = [f1_f2, f2_f3, f4_f5, f5_f6, f7_f8]

                if max(images) < self.threshold:
                    for aKey, aVal in ans_dict.iteritems():
                        diff = self.compare_images(figs[7].transpose(flip), ans_dict[aKey])
                        if diff < self.threshold:
                            solutions[aKey] = diff

        return solutions

    def test_growth(self, figs, ans_dict):
        # find best fit for an incremental growth problem
        solutions = {}

        # first get a black pixel count for each figure in the primary figures list and store that info
        try:
            bcountFig = {}
            fig_cnt = 1
            for k in figs:
                b, w = k.getcolors()
                bcountFig[str(fig_cnt)] = b
                fig_cnt += 1

            # do same for answers
            ks = ans_dict.keys()
            bcountAns = {}
            for j in ks:
                b, w = ans_dict[j].getcolors()
                bcountAns[j] = b

        # if there is only 1 color in the figure, skip the problem
        except ValueError:
            return solutions

        # method not applicable to 2x2 figures
        if len(figs) == 3:
            solutions = {}

        else:
            # check for growth between each figure
            s1_growth = False
            s2_growth = False
            s3_growth = False

            if bcountFig['1'][0] < bcountFig['2'][0] < bcountFig['3'][0]:
                s1_growth = True

            if bcountFig['4'][0] < bcountFig['5'][0] < bcountFig['6'][0]:
                s2_growth = True

            if bcountFig['7'][0] < bcountFig['8'][0]:
                s3_growth = True

            if s1_growth and s2_growth and s3_growth:
                for aKey, aVal in ans_dict.iteritems():
                    if bcountFig['8'][0] < bcountAns[aKey][0]:
                        solutions[aKey] = self.compare_images(figs[7], ans_dict[aKey])

        return solutions

    def raw_comparison(self, figs, ans_dict):
        # find best raw comparison using RMS difference
        solutions = {}
        best_distance = 9999.9

        if len(figs) == 3:
            set1_score = self.compare_images(figs[0], figs[1])

            for aKey, aVal in ans_dict.iteritems():
                set2_score = self.compare_images(figs[2], ans_dict[aKey])

                cur_distance = abs(set1_score - set2_score)

                if cur_distance <= best_distance:
                    best_distance = cur_distance
                    winner =  [aKey, best_distance]

            solutions[winner[0]] = winner[1]

        else:
            set1_score = 0
            set2_score = 0

            set1_score += self.compare_images(figs[0], figs[1])
            set1_score += self.compare_images(figs[1], figs[2])

            set2_score += self.compare_images(figs[3], figs[4])
            set2_score += self.compare_images(figs[4], figs[5])

            # check each possible answer and add each iteration of best distance to the solution list
            # take the final, and best, solution added, as that will be best possible distance
            for key, val in ans_dict.iteritems():
                set3_score = 0

                set3_score += self.compare_images(figs[6], figs[7])
                set3_score += self.compare_images(figs[7], ans_dict[key])

                cur_distance = (abs(set1_score - set3_score) + abs(set2_score - set3_score))

                if cur_distance <= best_distance:
                    best_distance = cur_distance
                    winner = [key, best_distance]

            solutions[winner[0]] = winner[1]

        return solutions
