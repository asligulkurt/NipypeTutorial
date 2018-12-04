from psychopy import visual, core, event
import math, random, sys, os
import numpy as np

class Wedge_Experiment:
    def __init__(self, initial_duration_in_seconds, final_duration_in_seconds, number_of_trials, flickering_duration_in_seconds, 
            blank_duration_in_seconds, flickering_rate, wedge_size_in_degree, unvisible_wedge_size_in_degree, TR, log_filename, fixation_log_filename):
        self.initial_duration_in_seconds = initial_duration_in_seconds
        self.final_duration_in_seconds = final_duration_in_seconds
        self.number_of_trials = number_of_trials#self.check_if_even_and_so_return(number_of_trials)
        self.flickering_duration_in_seconds = flickering_duration_in_seconds
        self.blank_duration_in_seconds = blank_duration_in_seconds
        self.flickering_rate = flickering_rate
        self.window_size_x = 1920
        self.window_size_y = 1080
        self.inner_wedge_size = wedge_size_in_degree
        self.unvisible_inner_wedge_size = unvisible_wedge_size_in_degree
        self.clock = None
        self.TR_in_seconds = TR
        self.log_filename = log_filename
        self.target = os.open(log_filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        self.fixation_target = os.open(fixation_log_filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        self.trigger_key = '6'
        self.yellow_button = '2'
        self.blue_button = '3'
        self.exit_key = 'escape'
        self.possible_fixation_blocks_in_TRs = [7,8,9]
        self.possible_fixation_colors = ['yellow','blue']
        #self.arrow_left_v = 0.4 * np.array([[.8, 0], [.6, .2], [.6, -.2], [-.6, .2], [-.6, -.2], [.6, -.4], [.6, .4], [.8, 0]])
        #self.arrow_v=0.4*np.array([[.6, 0], [.4, -.1], [.4, .1], [-.4, .1], [-.4, -.1], [.6, 0]])


    def check_if_even_and_so_return(self, number_of_trials):
        if number_of_trials % 2 is 0:
            return number_of_trials
        elif number_of_trials % 2 is not 0:
            sys.exit("error: the program is terminated since number of trials is not even. restart the program by entering correct parameters!")
        else:
            print("error in check_if_even_and_so_return().")

    def setup(self):
        core.checkPygletDuringWait = False
        self.create_window()
        self.left_arrow = visual.ImageStim(win=self.mywin, size=(7, 7), image="D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/experiment_7/LT_14_log_data/fMRI_hands_on_session/left-arrow.jpg")
        self.right_arrow = visual.ImageStim(win=self.mywin, size=(7, 7), image="D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/experiment_7/LT_14_log_data/fMRI_hands_on_session/right-arrow.jpg")
        self.left_right_arrow = visual.ImageStim(win=self.mywin, size=(7, 7), image="D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/experiment_7/LT_14_log_data/fMRI_hands_on_session/left-right-arrow.jpg")
        self.blank_arrow = visual.ImageStim(win=self.mywin, size=(7, 7), image="D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/experiment_7/LT_14_log_data/fMRI_hands_on_session/blank-arrow.jpg")
        event.Mouse(visible=False)

        self.block_duration_in_seconds = self.flickering_duration_in_seconds + self.blank_duration_in_seconds
        self.total_flickering_and_blank_durations_in_seconds = (self.flickering_duration_in_seconds + self.blank_duration_in_seconds) * self.number_of_trials/2
        self.experiment_duration_in_seconds = (self.initial_duration_in_seconds + self.final_duration_in_seconds +  self.total_flickering_and_blank_durations_in_seconds)*1.0
        print("initial blank duration: %s" % self.initial_duration_in_seconds)
        print("final blank duration: %s" % self.final_duration_in_seconds)
        print("number of trials (L-R not together): %s" % self.number_of_trials)
        print("flickering duration: %s" % self.flickering_duration_in_seconds)
        print("blank duration: %s" % self.blank_duration_in_seconds)
        print("total_flickering_and_blank_durations_in_seconds duration: %s" % self.total_flickering_and_blank_durations_in_seconds)
        print("experiment duration in seconds: %s" % str(self.total_flickering_and_blank_durations_in_seconds + self.initial_duration_in_seconds + self.final_duration_in_seconds))
        print("TR value: %s" % self.TR_in_seconds)

        self.frame_rate = 60
        self.one_frame_duration_in_seconds = 1.0/self.frame_rate

        self.experiment_duration_in_TRs = int(self.experiment_duration_in_seconds / self.TR_in_seconds)
        self.total_flickering_and_blank_durations_in_TRs =  self.total_flickering_and_blank_durations_in_seconds*1.0 / self.TR_in_seconds
        self.flickering_duration_in_TRs = self.flickering_duration_in_seconds*1.0 / self.TR_in_seconds
        self.flickering_duration_in_frames = self.flickering_duration_in_seconds * self.frame_rate
        self.blank_duration_in_TRs = self.blank_duration_in_seconds*1.0 / self.TR_in_seconds
        self.block_duration_in_TRs = self.block_duration_in_seconds*1.0  / self.TR_in_seconds
        self.initial_duration_in_TRs =  self.initial_duration_in_seconds*1.0 / self.TR_in_seconds
        self.final_duration_in_TRs =  self.final_duration_in_seconds*1.0 / self.TR_in_seconds
        self.number_of_flickering_states = self.flickering_duration_in_TRs * self.number_of_trials
        self.number_of_blank_states = self.blank_duration_in_TRs * self.number_of_trials
        self.number_of_flickering_and_blank_states =  self.number_of_flickering_states + self.number_of_blank_states
        self.number_of_total_states = self.initial_duration_in_TRs + self.final_duration_in_TRs + self.number_of_flickering_and_blank_states

        self.TRs_where_state_changes = self.specify_TRs_where_state_changes()
        #self.states = self.create_and_shuffle_states()
        self.states = self.create_states()
        #print ('aa:', len(self.states), len(self.TRs_where_state_changes))
        #exit()
        os.write(self.target, str(self.states)+'\n')
        os.write(self.target, str(self.TRs_where_state_changes)+'\n')

        self.TRs_to_states = self.create_TRs_to_states(self.TRs_where_state_changes, self.states)

        self.log_data = self.create_log_data()
        self.create_log_fixation_response_data()

        print("TRs: ",self.TRs_where_state_changes)
        print("experiment duration in TRs: %s (has to be integer)" % str(self.total_flickering_and_blank_durations_in_TRs + self.initial_duration_in_TRs + self.final_duration_in_TRs))
        print("experiment duration in TRs: %s (has to be integer)" % str(self.experiment_duration_in_TRs))
        
        noise = np.random.normal(0, 1, self.experiment_duration_in_TRs)
        #self.all_TRs = [((i+1)*250 + noise[i])/1000 for i in range(self.experiment_duration_in_TRs)]
        self.all_TRs = [((i + 1) * 2) for i in range(self.experiment_duration_in_TRs)]
        print('all_TRs: ',self.all_TRs)

        if self.flickering_duration_in_seconds < self.TR_in_seconds:
            self.number_of_frames_flickered_in_each_TR = self.frame_rate*self.flickering_duration_in_seconds
            self.number_of_frames_for_blank_in_each_TR = self.frame_rate*(self.TR_in_seconds-self.flickering_duration_in_seconds)
        else:
            self.number_of_frames_flickered_in_each_TR = int(self.frame_rate*self.TR_in_seconds)
            self.number_of_frames_for_blank_in_each_TR = 0

    def create_window(self):
        self.mywin = visual.Window(size=[self.window_size_x,self.window_size_y], fullscr = True, monitor="testMonitor", units="deg")
    
    def initialize_wedges_and_fixation(self):
        self.initialize_wedges()
        self.initialize_fixation()

    def initialize_wedges(self):        
        self.right_wedge = visual.RadialStim(win=self.mywin, tex='sqrXsqr', color=1, contrast=0.4, size=self.inner_wedge_size,
            visibleWedge=[45, 135], radialCycles=8, angularCycles=16, interpolate=False,
            autoLog=False)

        self.right_unvisible_wedge = visual.RadialStim(win=self.mywin, tex='sqrXsqr', mask='circle', color='grey', contrast=0, size=self.unvisible_inner_wedge_size,
            visibleWedge=[45, 135], radialCycles=8, angularCycles=16, interpolate=False,
            autoLog=False)

        self.left_wedge = visual.RadialStim(win=self.mywin, tex='sqrXsqr', color=1, contrast=0.4, size=self.inner_wedge_size,
            visibleWedge=[225, 315], radialCycles=8, angularCycles=16, interpolate=False,
            autoLog=False)

        self.left_unvisible_wedge = visual.RadialStim(win=self.mywin, tex='sqrXsqr', mask='circle', color='grey', contrast=0, size=self.unvisible_inner_wedge_size,
            visibleWedge=[225, 315], radialCycles=8, angularCycles=16, interpolate=False,
            autoLog=False)

    def initialize_fixation(self): 
        self.fixation = visual.GratingStim(win=self.mywin, mask='circle', size=0.12, pos=[0,0], sf=0, rgb='red') # contrast ve size ??

    def draw_wedges_and_fixation(self):
        #self.right_wedge.draw()
        #self.right_unvisible_wedge.draw()
        #self.left_wedge.draw()
        #self.left_unvisible_wedge.draw()
        self.fixation.draw()
        self.mywin.flip()

    def specify_TRs_where_state_changes(self):
        TRs_where_state_changes = []
        temp_TR = self.initial_duration_in_TRs
        is_TR_for_flickering = True
        is_TR_for_blank = False
        while temp_TR < self.experiment_duration_in_TRs - self.final_duration_in_TRs:
            TRs_where_state_changes.append(int(temp_TR))
            if is_TR_for_flickering:
                temp_TR = temp_TR + self.flickering_duration_in_TRs
                is_TR_for_flickering = False
                is_TR_for_blank = True
            elif is_TR_for_blank:
                temp_TR = temp_TR + self.blank_duration_in_TRs
                is_TR_for_blank = False
                is_TR_for_flickering = True
            else:
                print("Error in specify_TRs_where_state_changes()")
        return TRs_where_state_changes

    def create_states(self):
        stims = ['L', 'R', 'L-R', 'B']
        states = []
        for TR in range(int(self.number_of_trials)):
            remaining = TR % 4
            if remaining == 0:
                states.append(stims[0])
            elif remaining == 1:
                states.append(stims[1])
            elif remaining == 2:
                states.append(stims[2])
            elif remaining == 3:
                states.append(stims[3])

        print("states: ", states)
        #random.shuffle(states)
        #print("random states: ", states)

        '''
        for TR in range(int(2*self.number_of_trials)):
            if states[TR]=='L' or states[TR]=='R':
                states.insert(TR+1, 'B')
            elif states[TR]=='B':
                continue
            else:
                print("Error in create and shuffle states")
        '''
        print("states with blanks: ", states)
        return states

    def create_and_shuffle_states(self):
        states = []
        for TR in range(int(self.number_of_trials)):
            remaining = TR % 2
            if remaining == 0:
                states.append('L')
            elif remaining == 1:
                states.append('R')

        print("states: ", states)
        random.shuffle(states)
        print("random states: ", states)

        for TR in range(int(2*self.number_of_trials)):
            if states[TR]=='L' or states[TR]=='R':
                states.insert(TR+1, 'B')
            elif states[TR]=='B':
                continue
            else:
                print("Error in create and shuffle states")

        #print("states with blanks: ", states)
        return states

    def shuffle_states(self):
        random.shuffle(self.all_states)

    def create_TRs_to_states(self, TRs, states):
        TRs_to_states = {}
        for TR_index in range(len(TRs)):
            TRs_to_states[TRs[TR_index]] = states[TR_index]
        print("TRs to states: ",TRs_to_states)
        return(TRs_to_states)

    def record_fixation_task(self, key_timestamp, TR):
        if key_timestamp:
            for key_time in key_timestamp:
                if key_time[0] == self.blue_button:
                    self.log_fixation_response_data[TR]['response'] = 'blue'
                elif key_time[0] == self.yellow_button:
                    self.log_fixation_response_data[TR]['response'] = 'yellow'

    def create_log_data(self):
        log_data = {}
        for TR in range(int(self.experiment_duration_in_TRs)):
          log_data[TR] = {}
          log_data[TR]['tr'] = None
          log_data[TR]['t_t'] = None
          log_data[TR]['s_t'] = None
          log_data[TR]['state'] = None
        return log_data

    def create_log_fixation_response_data(self):
        self.log_fixation_response_data = {}
        for TR in range(int(self.experiment_duration_in_TRs)):
          self.log_fixation_response_data[TR] = {}
          self.log_fixation_response_data[TR]['actual'] = None
          self.log_fixation_response_data[TR]['response'] = None

    def run(self):
        current_TR = 0
        self.current_state = 'B'
        self.initialize_wedges_and_fixation()
        self.isNextTriggerLate = False
        self.prev_current_state = 'B'
        self.prev_TR = -1

        key_timestamp = self.waitForTriggerKeyAndWriteToFile()
        if key_timestamp: # for the first TR
          if self.trigger_key in key_timestamp[0]:
            trigger_time = [key_timestamp[0][1]]
            next_trigger_time = []
            self.add_log_into_data(current_TR, trigger_time=trigger_time, current_state='B')

        #self.draw_wedges_and_fixation()
        while(current_TR < int(self.experiment_duration_in_TRs)):
            #print(current_TR)
            #print(self.current_state)
            self.run_fixation_task(current_TR)

            #print('runin basindaki: ',current_TR, self.clock.getTime(), next_trigger_time)
            
            if next_trigger_time:
                #print ('1')
                self.add_log_into_data(current_TR, trigger_time=next_trigger_time) # for the current trigger

            next_trigger_time, stim_time = self.flicker_or_rest(current_TR, next_trigger_time) # next_trigger_time is for current_TR+1, stim_time is for current_TR

            #print('stim_time_2: ', stim_time ,current_TR, next_trigger_time)
            if stim_time:
              #print('55555555555555555555')
              if not self.isNextTriggerLate:
                #print (current_TR, stim_time, self.current_state)
                #print('6666666666666666666')
                self.add_log_into_data(current_TR, stim_time=stim_time, current_state=self.current_state) # for the current trigger
              else:
                #print('777777777777777777')
                if len(next_trigger_time)==1: # next next trigger is also late
                  #print('1asd1:')
                  print(current_TR, next_trigger_time, stim_time, self.current_state)
                  #self.add_log_into_data(current_TR, trigger_time=next_trigger_time) # for the current trigger # takes next_trigger_time[0], so it is correct
                  #self.add_log_into_data(current_TR, stim_time=stim_time, current_state=self.current_state) # for the current trigger
                  self.add_log_into_data(current_TR, trigger_time=next_trigger_time, stim_time=stim_time, current_state=self.current_state)
                  self.isNextTriggerLate = True
                elif len(next_trigger_time)==2: # next next trigger is not late (i.e., came earlier or at 250 ms)
                  #print('2asd2:')
                  print(current_TR, next_trigger_time, stim_time, self.current_state)
                  self.add_log_into_data(current_TR, trigger_time=next_trigger_time, stim_time=stim_time, current_state=self.current_state) # for the current trigger, trigger came late
                  #self.add_log_into_data(current_TR, stim_time=stim_time, current_state=self.current_state) # for the current trigger
                  self.isNextTriggerLate = False
                elif len(next_trigger_time)==0: # next trigger still didn't come. trigger miss!
                    #print('0asd0:')
                    self.isNextTriggerLate = True
                    #print("next trigger still didn't come. trigger miss!", str(current_TR), self.current_state)
                    self.add_log_into_data(current_TR, current_state=self.current_state)
                else: 
                    print('error in run(). next_trigger_time length is not as expected.')
                    exit()

            if len(next_trigger_time)==0: # trigger came later than 250 ms in flickering state
              self.isNextTriggerLate = True

            if not self.isStateUpdated(current_TR+1): # for the next TR 
              self.prev_TR = current_TR # for exception
              self.prev_current_state = self.current_state # for exception
              self.update_state(current_TR+1)
              self.add_log_into_data(current_TR+1, current_state=self.current_state)

            current_TR = current_TR + 1

        experiment_finish_time = self.clock.getTime()
        self.write_to_file(experiment_finish_time)

    def waitForTriggerKeyAndWriteToFile(self):
        key = event.waitKeys(keyList=[self.trigger_key, self.exit_key])
        if key[0] == self.exit_key:
            core.quit()
        self.clock = core.Clock()
        key_timestamp = [(key[0], self.clock.getTime())]
        os.write(self.target, "Experiment Start Time: "+str(key_timestamp[0][1])+"\n")
        os.write(self.target, "     #TR                   TR(s)                  Trigger_Time(s)                 Stimulus_Time(s)              Stimulus_Type\n      ")
        return key_timestamp

    def run_fixation_task(self, current_TR):
        if (current_TR % self.possible_fixation_blocks_in_TRs[1]) == 0:
          self.fixation.setColor(self.possible_fixation_colors[0])
          self.log_fixation_response_data[current_TR]['actual'] = self.possible_fixation_colors[0]

        #elif (current_TR % self.possible_fixation_blocks_in_TRs[1]) == 1: # next TR
        else:
          self.fixation.setColor('red')
          random.shuffle(self.possible_fixation_blocks_in_TRs)
          random.shuffle(self.possible_fixation_colors)

    def flicker_or_rest(self, current_TR, next_trigger_time):
        # initial wait state
        if current_TR < self.initial_duration_in_TRs:
           #print("initial wait state")
           next_trigger_time, stim_time = self.rest(current_TR, next_trigger_time)
        # final wait state
        elif (current_TR >= (self.initial_duration_in_TRs + self.total_flickering_and_blank_durations_in_TRs)):
           #print("final wait state")
           next_trigger_time, stim_time = self.rest(current_TR, next_trigger_time)
        # stimulus state
        elif self.current_state == 'L' or self.current_state == 'R' or self.current_state == 'L-R':
        #elif ((current_TR - self.initial_duration_in_TRs) % self.block_duration_in_TRs) < self.flickering_duration_in_TRs:
           #print("flickering state")
           key_timestamp = event.getKeys(keyList=[self.trigger_key, self.exit_key], timeStamped=self.clock)
           if key_timestamp:
            print(current_TR, 'flicker', self.clock.getTime(), key_timestamp[0][1])
            next_trigger_time.append(key_timestamp[0][1])
            #self.isNextTriggerLate = False
            self.add_log_into_data(current_TR, trigger_time=next_trigger_time, stim_time=self.clock.getTime(), current_state=self.current_state)
           else:
            print(current_TR, 'flicker', self.clock.getTime(), None)

           next_trigger_time, stim_time = self.flicker(current_TR, next_trigger_time)
        # resting state
        elif self.current_state == 'B':
        #elif ((current_TR - self.initial_duration_in_TRs) % self.block_duration_in_TRs) >= self.flickering_duration_in_TRs:
           #print("resting state")
           key_timestamp = event.getKeys(keyList=[self.trigger_key, self.exit_key], timeStamped=self.clock)
           if key_timestamp:
            #print(current_TR, 'rest', self.clock.getTime(), key_timestamp[0][1])
            next_trigger_time.append(key_timestamp[0][1])
            self.isNextTriggerLate = False
            self.add_log_into_data(current_TR, trigger_time=next_trigger_time, stim_time=self.clock.getTime(), current_state=self.current_state)
           else:
            print(current_TR, 'rest', self.clock.getTime(), None)
           next_trigger_time, stim_time = self.rest(current_TR, next_trigger_time)
        else:
           print("Error in flicker_or_rest() function")
        return next_trigger_time, stim_time

    def isStateUpdated(self, TR):
        if TR in self.TRs_where_state_changes:
            return False
        else:
            return True

    def update_state(self, TR):
        if self.TRs_to_states[TR]:
            self.current_state = self.TRs_to_states[TR]
        else:
            print("Error in update state.")

    def write_to_file(self, experiment_finish_time):#(self, current_TR=None, trigger_time=None, stim_time=None):
        for TR in self.log_data:
          os.write(self.target, str(TR)+"                      ")
          os.write(self.target, str(self.log_data[TR]['tr'])+"                 ")
          os.write(self.target, str(self.log_data[TR]['t_t'])+"                  ")
          os.write(self.target, str(self.log_data[TR]['s_t'])+"                  ")
          os.write(self.target, str(self.log_data[TR]['state'])+"\n"+"      ")

        os.write(self.target, "\nExperiment Finish Time: "+str(experiment_finish_time))
        os.write(self.target, "\nExperiment Expected Finish Time: "+str(self.experiment_duration_in_seconds))
        os.write(self.target, "\nExperiment Expected Finish TR: " +str(self.experiment_duration_in_TRs))
        #self.target.flush()
        os.fsync(self.target)
        os.close(self.target)

        for TR in self.log_fixation_response_data:
            os.write(self.fixation_target, str(TR) + "                      ")
            os.write(self.fixation_target, str(self.log_fixation_response_data[TR]['actual']) + "                 ")
            os.write(self.fixation_target, str(self.log_fixation_response_data[TR]['response']) + "\n")
        os.fsync(self.fixation_target)
        os.close(self.fixation_target)

    def add_log_into_data(self, current_TR, trigger_time=None, stim_time=None, current_state=None):
        if current_TR == 0 or current_TR:
            self.log_data[current_TR]['tr'] = self.TR_in_seconds * current_TR
            if trigger_time:
                self.log_data[current_TR]['t_t'] = trigger_time.pop(0)
            if stim_time:
                self.log_data[current_TR]['s_t'] = stim_time
            if current_state:
                self.log_data[current_TR]['state'] = current_state
          #return trigger

    def flicker(self, current_TR, next_trigger_time):
        frame = 0
        first = True
        second = True
        #while frame < self.number_of_frames_flickered_in_each_TR:
        init_time = self.clock.getTime()
        init_frame = int(init_time / self.one_frame_duration_in_seconds)
        prev_frame = -1
        #while (self.all_TRs[current_TR] >= init_time):
        while frame < self.number_of_frames_flickered_in_each_TR:
            #key_timestamp = event.getKeys(keyList=[self.trigger_key, self.blue_button, self.yellow_button, self.exit_key], timeStamped=self.clock)
            #self.record_fixation_task(key_timestamp, current_TR)
            if self.current_state == 'L':
                current_time = self.clock.getTime()
                if ((frame % (2*self.flickering_rate)) == 0):
                    #self.left_wedge.setColor(1)
                    if first:
                        if frame == 0:
                            stim_time = self.clock.getTime()
                            print('stim_time: ', stim_time)
                        self.left_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        first = False
                elif ((frame % (2 * self.flickering_rate)) == self.flickering_rate):
                    #self.left_wedge.setColor(-1)
                    if second:
                        self.left_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        second = False
            elif self.current_state == 'R':
                current_time = self.clock.getTime()
                if ((frame % (2*self.flickering_rate)) == 0):
                    #self.right_wedge.setColor(1)
                    if first:
                        if frame == 0:
                            stim_time = self.clock.getTime()
                            print('stim_time: ', stim_time)
                        self.right_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        first = False
                elif ((frame % (2 * self.flickering_rate)) == self.flickering_rate):
                    #self.right_wedge.setColor(-1)
                    if second:
                        self.right_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        second = False
            elif self.current_state == 'L-R':
                current_time = self.clock.getTime()
                if ((frame % (2*self.flickering_rate)) == 0):
                    #self.left_wedge.setColor(1)
                    #self.right_wedge.setColor(1)
                    if first:
                        if frame == 0:
                            stim_time = self.clock.getTime()
                            print('stim_time: ', stim_time)
                        self.left_right_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        first = False
                elif ((frame % (2 * self.flickering_rate)) == self.flickering_rate):
                    #self.left_wedge.setColor(-1)
                    #self.right_wedge.setColor(-1)
                    if second:
                        self.left_right_arrow.draw(win=self.mywin)
                        self.draw_wedges_and_fixation()
                        second = False
            else:
                print('Error: undefined state. neither Inn, Out.', self.current_state)
                exit()

            if frame == 0:
                if self.log_data[current_TR]['s_t'] == None:
                    self.log_data[current_TR]['s_t'] = str(stim_time)

            #self.draw_wedges_and_fixation()
            #if (current_time - init_time) >= (self.one_frame_duration_in_seconds):
            frame = int(current_time/self.one_frame_duration_in_seconds) - init_frame
            if not(prev_frame == frame):
                #init_time = current_time
                first = True
                second = True
                prev_frame = frame
                #frame += 1

            #print("flicker ", current_TR)
            #print('flicker1', frame, self.all_TRs[current_TR], self.clock.getTime(), abs(self.all_TRs[current_TR] - self.clock.getTime()))
            #print(current_TR, self.clock.getTime(), next_trigger_time, stim_time, 'flicker', frame)
            #if (self.all_TRs[current_TR] - self.clock.getTime()) < 0.0001:


        print(current_TR, self.clock.getTime(), 'flicker1')
        key_timestamp = event.getKeys(keyList=[self.trigger_key, self.blue_button, self.yellow_button, self.exit_key], timeStamped=self.clock) # for 2, 3, 4th frames
        if key_timestamp:
            print(current_TR, self.clock.getTime(), key_timestamp[0][1], 'flicker2')
        else:
            print(current_TR, self.clock.getTime(), None, 'flicker2')

        self.record_fixation_task(key_timestamp, current_TR)
        #self.draw_wedges_and_fixation()
            #event.clearEvents('all')

        if key_timestamp:
            for key_time in key_timestamp:
                #print ('key time ', key_time)
                #print ('next trigger time ', next_trigger_time)
                if key_time[0] == self.trigger_key:
                    if len(next_trigger_time) == 0:
                        next_trigger_time.append(key_time[1])
                    elif abs(self.all_TRs[current_TR] - next_trigger_time[0]) > abs(self.all_TRs[current_TR] - key_time[1]):
                        next_trigger_time = []
                        next_trigger_time.append(key_time[1])
                elif key_time[0] == self.exit_key:
                    experiment_finish_time = self.clock.getTime()
                    self.write_to_file(experiment_finish_time)
                    print("exit TR: ",current_TR)
                    core.quit()

        print ('next_trigger time, stim_time: ',next_trigger_time, stim_time)
        if len(next_trigger_time) == 0: # trigger become late, so wait until trigger comes
            self.isNextTriggerLate = True

        return next_trigger_time, stim_time

    def rest(self, current_TR, next_trigger_time):
        frame = 0
        #while True:
        init_time = self.clock.getTime()
        previous_time = init_time
        #print (self.all_TRs[current_TR], init_time)
        #while frame < self.number_of_frames_flickered_in_each_TR:
        '''
        print ('a: ',self.all_TRs[current_TR], init_time, self.TR_in_seconds)
        while (self.all_TRs[current_TR] >= previous_time):
            if frame == 0:
                stim_time = self.clock.getTime()
                if self.log_data[current_TR]['s_t']==None:
                    self.log_data[current_TR]['s_t']= str(stim_time)
                print('TR, stim_time and trigger_time: ', current_TR, self.log_data[current_TR]['s_t'], self.log_data[current_TR]['t_t'])
                self.draw_wedges_and_fixation()
                #print("stim time ",stim_time, current_TR, next_trigger_time)

            #################

            # current_time = self.clock.getTime()
            key_timestamp = event.getKeys(keyList=[self.trigger_key, self.yellow_button, self.blue_button, self.exit_key], timeStamped=self.clock)
            self.record_fixation_task(key_timestamp, current_TR)
            # print ('rest: ', self.clock.getTime(), key_timestamp)

            # event.clearEvents('all')
            # print(current_TR, self.clock.getTime(), 'rest')
            if self.isNextTriggerLate and key_timestamp:
                for key_time in key_timestamp:
                    if key_time[0] == self.trigger_key:
                        next_trigger_time.append(key_time[1])
                        print ('restteki :', current_TR, next_trigger_time, stim_time, self.current_state)
                        self.add_log_into_data(current_TR, trigger_time=next_trigger_time, stim_time=stim_time,
                                               current_state=self.current_state)
                        self.isNextTriggerLate = False
                        print ('aaa: ', key_time)
                    elif key_time[0] == self.exit_key:
                        experiment_finish_time = self.clock.getTime()
                        self.write_to_file(experiment_finish_time)
                        print("exit TR: ", current_TR)
                        core.quit()
            elif (not self.isNextTriggerLate) and key_timestamp:
                for key_time in key_timestamp:
                    if key_time[0] == self.trigger_key:
                        print(current_TR, '2')
                        next_trigger_time.append(key_time[1])
                        self.isNextTriggerLate = False
                        # return next_trigger_time, stim_time
                    elif key_time[0] == self.exit_key:
                        experiment_finish_time = self.clock.getTime()
                        self.write_to_file(experiment_finish_time)
                        print("exit TR: ", current_TR)
                        core.quit()

            # after last trigger, it has to return after 0.25 s, but it waits another trigger to return. so when it is in last TR, i return the function after 0.25 s
            if current_TR == self.experiment_duration_in_TRs - 1 and self.clock.getTime > self.experiment_duration_in_seconds:
                core.wait(secs=self.TR_in_seconds, hogCPUperiod=0)
                self.log_data[current_TR]['state'] = 'B'
                return [], None


            ################
            # frame = frame + 1
            #if (current_time - init_time) >= (self.one_frame_duration_in_seconds):
            #print('frame: ', frame, current_TR, self.all_TRs[current_TR], init_time)

            current_time = self.clock.getTime()
            if (current_time - previous_time) >= self.one_frame_duration_in_seconds:
                previous_time = current_time
                print('frame: ', frame, current_TR, self.all_TRs[current_TR], init_time, previous_time, current_time)
                first = True
                second = True
                frame += 1
        
        return next_trigger_time, stim_time
        '''
        frame = 0
        while True:
            if frame == 0:
                stim_time = self.clock.getTime()
                self.blank_arrow.draw(win=self.mywin)
                self.draw_wedges_and_fixation()
                #os.write(self.target, str(self.clock.getTime()) + "\n      ")
                #os.fsync(self.target)

            key_timestamp = event.getKeys(keyList=[self.trigger_key, self.exit_key], timeStamped=self.clock)
            # print(key_timestamp)
            if key_timestamp and key_timestamp[0][0] == self.trigger_key and ((self.clock.getTime() - stim_time) > self.TR_in_seconds/2):
                next_trigger_time.append(key_timestamp[0][1])
                return next_trigger_time, stim_time
            elif (key_timestamp and key_timestamp[0][0] == self.exit_key) or current_TR == self.experiment_duration_in_TRs - 1:
                print("exit TR: ", current_TR)
                self.log_data[current_TR]['state'] = 'B'
                self.log_data[current_TR]['s_t'] = stim_time
                core.wait(secs=self.TR_in_seconds, hogCPUperiod=0)
                experiment_finish_time = self.clock.getTime()
                self.write_to_file(experiment_finish_time)
                print("exit TR: ", current_TR)
                core.quit()

            #self.left_wedge1.setColor(self.left_wedge1.color)
            #self.right_wedge1.setColor(self.right_wedge1.color)
            #self.draw_wedges_and_fixation()
            frame = frame + 1

if __name__ == "__main__":
    experiment_id = 'experiment_7'
    subject_id = 'LT_14'
    session_type = 'functional_localizer' # impulse, or longer_pulse for both experiment 2 and experiment 3
    epi_type = 'mb_epi' # mb_epi for experiment 4 ||| mb_epi, normal_epi for experiment 3 ||| mb_epi for experiment 2
    TR_in_seconds = 2 # 0.25 or 2

    initial_duration_in_seconds = 20 # 20
    final_duration_in_seconds = 10 # 10
    flickering_duration_in_seconds = 12 # 1
    blank_duration_in_seconds = 12 # 32-1, 26-1, 24-1, 20-1
    number_of_trials = 20 # 5 Inn - 5 Out
    flickering_rate = 4

    run_id = 0 # granger deneyi basliyor, 0 (left-right) cekilecek

    wedge_size_in_degree = [12]
    unvisible_wedge_size_in_degree = [4]

    folder_name = 'fMRI_hands_on_session'

    log_filename = "D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/"+experiment_id+"/"+subject_id+"_log_data/"+folder_name+"/"+session_type+"_log_"+subject_id[-2:]+"_run_"+str(run_id)+"_motion.txt"
    fixation_log_filename = "D:/cembe_yedek/Documents/Master/Code/newest_exp2_exp3_exp4/prt_log_files/"+experiment_id+"/"+subject_id+"_log_data/"+folder_name+"/"+session_type+"_log_"+subject_id[-2:]+"_run_"+str(run_id)+"_motion_fixation_log.txt"

    wedge_experiment = Wedge_Experiment(initial_duration_in_seconds, final_duration_in_seconds, number_of_trials, flickering_duration_in_seconds, 
        blank_duration_in_seconds, flickering_rate, wedge_size_in_degree[run_id], unvisible_wedge_size_in_degree[run_id], TR_in_seconds, log_filename, fixation_log_filename)

    wedge_experiment.setup()
    wedge_experiment.run()
    # % 50 contrast = 0.24193548387
    # % 25 contrast = 0.11462450592
    # % 40 contrast = 0.18577
    # new % 40 contrast = 0.3637
    # new 2 % 40 contrast = 0.4