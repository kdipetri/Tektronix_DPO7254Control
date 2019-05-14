# TimingAnalysis

Code for timing analysis. Author: **Nicola Minafra**

* source ../includes.CMSTimingSetup.sh
* Usage:
```
$> make
$> ./example_analyzeData --help
  Allowed options:
        std::cout << "List of options: " << std::endl;
        std::cout << "-h [ --help ]                     produce help message" << std::endl;
        std::cout << "-f [ --channel ] (=0)             channel to analyze" << std::endl;
        std::cout << "-k [ --configuration ]       Global congif to analyze" << std::endl;
        std::cout << "-c [ --cfd_threshold ] (=0.4)     CFD fraction" << std::endl;
        std::cout << "                                  a negative value will start a scan with" << std::endl;
        std::cout << "                                  a step equal to |cfd_threshold|" << std::endl;
        std::cout << "-t [ --threshold ] (=-0.1)        Threshold, negative for" << std::endl;
        std::cout << "                                  negative signals (V)" << std::endl;
        std::cout << "-p [ --lowpass ] (=0)             Lowpass filter frequency (Hz)" << std::endl;
        std::cout << "-o [ --outputdir ] (=./Results)   output directory" << std::endl;
        std::cout << "-i [ --Run_config_in ]            Run_config.txt input file" << std::endl;
        std::cout << "-s [ --saturation ] (=0.2)        saturation cut for DUT" << std::endl;
        std::cout << "-n [ --namesensor ]               name of the sensor and board" << std::endl;
```
The code needs the name of the sensor, the output directory and the config file to operate correctly. The input file is also crucial: the analysis script requires a text file where are store all of the run and config number.

For Fermilab analysis:
```
$> ./example_analyzeData -i ../RunTable/Run_config.txt  -f 1 -t -0.03 -s 0.6 -c 0.5 --lowpass 700e6 -n HPK4x4prerad -O ./Results/
```

The output root file is saved in **Results/** with the same name of the input file, plus **_result_ch0_ch1.root**
Important plots:
- evN: graph of waveforms
- h_deltat_Smart: time difference between the two channels with the method ComputeExactTimeCFD in  `/TimingAnalysis/include/timingAlgorithm.h`
- h_max_selected_DetN: amplitude of only events selected for timing analysis
- h_SNR_DetN: SNR computed event by event


NOTE: Root required, <br />
on lxplus:
```
$> . /cvmfs/sft.cern.ch/lcg/releases/LCG_88/ROOT/6.08.06/x86_64-slc6-gcc62-opt/ROOT-env.sh
$> make

To run the analysis like it is:
$> . run_withLowpass.sh N

with N:0..26 to choose the input file:
0  : W5_LP_165V
1  : W5_LP_175V
2  : W5_LP_185V
3  : W5_LP_195V
4  : W5_LP_200V
5  : W5_LP_205V
6  : W5_LP8e14_315V
7  : W5_LP8e14_335V
8  : W5_LP8e14_355V
9  : W5_LP8e14_365V
10 : W5_LP8e14_375V
11 : W5_LP8e14_380V
12 : W5_LP8e14_390V
13 : W5_LP8e14_395V
14 : W5_LP8e14_400V
15 : W5_LP1p5e15_350V
16 : W5_LP1p5e15_370V
17 : W5_LP1p5e15_390V
18 : W5_LP1p5e15_400V
19 : W5_LP1p5e15_410V
20 : W5_LP1p5e15_415V
21 : W5_LP1p5e15_425V
22 : W5_LP1p5e15_435V
23 : W5_LP1p5e15_445V
24 : W5_LP1p5e15_455V
25 : W5_LP1p5e15_465V
26 : W5_LP1p5e15_485V

```
