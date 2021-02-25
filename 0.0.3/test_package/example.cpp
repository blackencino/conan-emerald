#include <emerald/shallow_weaver/simulation.h>

#include <iostream>

using namespace emerald::shallow_weaver;

int main(int argc, char *argv[]) {
  Simulation::Parameters params;
  Simulation simulation{params};

  for (int frame = 0; frame < simulation.parameters().num_batch_frames;
       ++frame) {
    simulation.step();
    std::cout << "Frame: " << frame << std::endl;
  }

  return 0;
}
