import {makeProject} from '@motion-canvas/core';

// import example from './scenes/example?scene';
import example from './scenes/claude-code-flow?scene';
import brollScene from './scenes/claude-workflow-broll?scene';

export default makeProject({
  scenes: [example, brollScene],
});
