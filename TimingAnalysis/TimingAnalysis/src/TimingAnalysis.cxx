#ifndef TimingAnalysis_cxx
#define TimingAnalysis_cxx

#include "TimingAnalysis.h"

//----------constructor-----------//

TimingAnalysis::TimingAnalysis(TTree * tree, const bool selectOnlyNewTracker, const float minTrackerX, const float maxTrackerX, const float minTrackerY, const float maxTrackerY): pulse(tree),
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
