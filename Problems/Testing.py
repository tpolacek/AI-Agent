str = 'poop'

if str != 'poop':
    print False
















'''
    # use solver method to find best possible solution to this orientation, and its similarity score
            solution1 = self.visual_solver_3x3(primary_figs, ans_dict, orientation1)
                solution2 = self.visual_solver_3x3(secondary_figs, ans_dict, orientation2)

                all_solutions = list(set(solution1) | set(solution2))
                common_solution = [val for val in solution1 if val in solution2]

                print problem.name
                print 'Primary Solution: ', solution1
                print 'Secondary Solution: ', solution2
                print

                #return int(solution1)

            else:
                orientation, figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight = \
                    self.group_3x3_visuals(img_dict, orient)

                primary_figs = [figOne, figTwo, figThree, figFour, figFive, figSix, figSeven, figEight]

                solution = self.visual_solver_3x3(primary_figs, ans_dict, orientation)

                print problem.name
                print 'Solution: ', solution
                print


        #solver method
                # list of possible solutions
        solutions = []

        # distance from the static answer sets
        best_distance = 99999

        if orientation != 'Diagonal':
            set1_score = 0
            set2_score = 0

            set1_score += self.compare_images(figs[0], figs[1])
            set1_score += self.compare_images(figs[1], figs[2])

            set2_score += self.compare_images(figs[3], figs[4])
            set2_score += self.compare_images(figs[4], figs[5])

            # check each possible answer and add each iteration of best distance to the solution list
            # take the final, and best, solution added, as that will be best possible distance
            # TODO maybe I don't want the lowest score, as it might pick answers where duplicates are there,
            # TODO but I don't want duplicates
            for aKey in ans_dict.keys():
                set3_score = 0

                set3_score += self.compare_images(figs[6], figs[7])
                set3_score += self.compare_images(figs[7], ans_dict[aKey])

                #solutions[aKey] = set3_score

                cur_distance = (abs(set1_score - set3_score) + abs(set2_score - set3_score))
                if cur_distance <= best_distance:
                    best_distance = cur_distance
                    #solutions[aKey] = cur_distance
                    solutions.append(aKey)

        else:
            set1_score = self.compare_images(figs[0], figs[1])
            set2_score = self.compare_images(figs[2], figs[3])
            set3_score = self.compare_images(figs[4], figs[5])

            for aKey in ans_dict.keys():
                set4_score = self.compare_images(figs[1], ans_dict[aKey])

                #solutions[aKey] = set4_score

                cur_distance = \
                    (abs(set1_score - set4_score) + abs(set2_score - set4_score) + abs(set3_score - set4_score))
                if cur_distance <= best_distance:
                    best_distance = cur_distance
                    #solutions[aKey] = cur_distance
                    solutions.append(aKey)

            #TODO can use solutions as a dictionary to return the similarity scores, but it fucks up several correct answers
            # return the solution one with lowest possible distance
            for sol, dist in solutions.iteritems():
                if dist == best_distance:
                    return sol, dist
            return solutions[-1]'''