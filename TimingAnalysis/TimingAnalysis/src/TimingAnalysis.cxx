#ifndef TimingAnalysis_cxx
#define TimingAnalysis_cxx

#include "TimingAnalysis.h"

//----------constructor-----------//

TimingAnalysis::TimingAnalysis(TTree * tree): pulse(tree, const bool selectOnlyNewTracker=false, const float minTrackerX=-1e9, const float maxTrackerX=1e9, const float minTrackerY=-1e9, const float maxTrackerY=1e9):
selectOnlyNewTracker_(selectOnlyNewTracker), minTrackerX_(minTrackerX), maxTrackerX_(maxTrackerX), minTrackerY_(minTrackerY), maxTrackerY_(maxTrackerY)
{}

//----------analysis methods------------//

void TimingAnalysis::initialize() {
  //Starting the watch
  std::cout << "*****************************************" << std::endl;
  m_timer.Start();
}

void TimingAnalysis::finalize() {
}

#endif
