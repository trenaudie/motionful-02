import {Circle, Layout, Rect, Node, makeScene2D, Txt, Line} from '@motion-canvas/2d';
import {
  all,
  createRef,
  easeInExpo,
  easeInOutExpo,
  waitFor,
  waitUntil,
  ThreadGenerator,
  chain,
  createSignal,
  slideTransition,
  Direction,
  easeOutCirc,
  createEaseInOutBack,
  range,
  InterpolationFunction,
  createComputed
} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  view.fill('#000000');

  // Create refs for all components
  const userInputBox = createRef<Rect>();
  const userInputText = createRef<Txt>();
  const claudeCliBox = createRef<Rect>();
  const claudeCliText = createRef<Txt>();
  const anthropicApiBox = createRef<Rect>();
  const anthropicApiText = createRef<Txt>();
  const toolsBox = createRef<Rect>();
  const toolsText = createRef<Txt>();
  const todoWriteBox = createRef<Rect>();
  const todoWriteText = createRef<Txt>();
  
  // Tool category boxes
  const coreFileOpsBox = createRef<Rect>();
  const coreFileOpsText = createRef<Txt>();
  const devToolsBox = createRef<Rect>();
  const devToolsText = createRef<Txt>();
  const webToolsBox = createRef<Rect>();
  const webToolsText = createRef<Txt>();
  const mcpBridgeBox = createRef<Rect>();
  const mcpBridgeText = createRef<Txt>();
  const mcpToolsBox = createRef<Rect>();
  const mcpToolsText = createRef<Txt>();
  const agentSystemBox = createRef<Rect>();
  const agentSystemText = createRef<Txt>();

  // Arrow refs
  const arrow1 = createRef<Line>();
  const arrow2 = createRef<Line>();
  const arrow3 = createRef<Line>();
  const arrow4 = createRef<Line>();
  const arrow5 = createRef<Line>();

  // Signals for dynamic positioning
  const centerX = createSignal(0);
  const centerY = createSignal(0);

  // Add all components to view
  view.add(
    <Node>
      {/* User Input */}
      <Rect
        ref={userInputBox}
        x={createComputed(() => centerX() - 400)}
        y={createComputed(() => centerY() + 200)}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={userInputText}
        x={createComputed(() => centerX() - 400)}
        y={createComputed(() => centerY() + 200)}
        text={'"Fix this bug"'}
        fontSize={16}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        opacity={0}
      />

      {/* Claude CLI */}
      <Rect
        ref={claudeCliBox}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY())}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={claudeCliText}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY())}
        text={'Claude CLI\n(claude-code)'}
        fontSize={16}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Anthropic API */}
      <Rect
        ref={anthropicApiBox}
        x={createComputed(() => centerX() + 400)}
        y={createComputed(() => centerY())}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={anthropicApiText}
        x={createComputed(() => centerX() + 400)}
        y={createComputed(() => centerY())}
        text={'Anthropic API\n(Claude)'}
        fontSize={16}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Tools Box */}
      <Rect
        ref={toolsBox}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY() + 200)}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={toolsText}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY() + 200)}
        text={'Tool Execution\n(Read, Edit, Bash)'}
        fontSize={14}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* TodoWrite */}
      <Rect
        ref={todoWriteBox}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY() + 350)}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={todoWriteText}
        x={createComputed(() => centerX())}
        y={createComputed(() => centerY() + 350)}
        text={'TodoWrite\n(Task Planning)'}
        fontSize={14}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Core File Operations */}
      <Rect
        ref={coreFileOpsBox}
        x={createComputed(() => centerX() - 300)}
        y={createComputed(() => centerY() + 350)}
        width={220}
        height={120}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={coreFileOpsText}
        x={createComputed(() => centerX() - 300)}
        y={createComputed(() => centerY() + 350)}
        text={'Core File Operations\n(Read, Edit, MultiEdit,\nWrite, Glob, Grep, LS)'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Development Tools */}
      <Rect
        ref={devToolsBox}
        x={createComputed(() => centerX() + 300)}
        y={createComputed(() => centerY() + 350)}
        width={200}
        height={100}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={devToolsText}
        x={createComputed(() => centerX() + 300)}
        y={createComputed(() => centerY() + 350)}
        text={'Development Tools\n(Bash, Notebooks)'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Web Tools */}
      <Rect
        ref={webToolsBox}
        x={createComputed(() => centerX() + 500)}
        y={createComputed(() => centerY() - 200)}
        width={180}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={webToolsText}
        x={createComputed(() => centerX() + 500)}
        y={createComputed(() => centerY() - 200)}
        text={'Web Tools\n(WebFetch, WebSearch)'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* MCP Bridge */}
      <Rect
        ref={mcpBridgeBox}
        x={createComputed(() => centerX() - 350)}
        y={createComputed(() => centerY() - 100)}
        width={160}
        height={60}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={mcpBridgeText}
        x={createComputed(() => centerX() - 350)}
        y={createComputed(() => centerY() - 100)}
        text={'MCP Bridge'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* MCP Tools */}
      <Rect
        ref={mcpToolsBox}
        x={createComputed(() => centerX() - 400)}
        y={createComputed(() => centerY() - 200)}
        width={200}
        height={100}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={mcpToolsText}
        x={createComputed(() => centerX() - 400)}
        y={createComputed(() => centerY() - 200)}
        text={'MCP Tools\n(IDE Diagnostics,\nCode Execution)'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Agent System */}
      <Rect
        ref={agentSystemBox}
        x={createComputed(() => centerX() + 300)}
        y={createComputed(() => centerY() + 500)}
        width={200}
        height={80}
        fill={'#ffffff'}
        stroke={'#e2e8f0'}
        lineWidth={1}
        radius={6}
        shadowColor={'#0000001a'}
        shadowOffset={[0, 1]}
        shadowBlur={3}
        opacity={0}
      />
      <Txt
        ref={agentSystemText}
        x={createComputed(() => centerX() + 300)}
        y={createComputed(() => centerY() + 500)}
        text={'Agent System\n(Task, ExitPlanMode)'}
        fontSize={12}
        fontFamily={'Inter, -apple-system, BlinkMacSystemFont, sans-serif'}
        fontWeight={500}
        fill={'#0f172a'}
        textAlign={'center'}
        opacity={0}
      />

      {/* Arrows */}
      <Line
        ref={arrow1}
        points={[
          [centerX() - 300, centerY() + 200],
          [centerX() - 100, centerY() + 40]
        ]}
        stroke={'#64748b'}
        lineWidth={2}
        endArrow
        opacity={0}
      />

      <Line
        ref={arrow2}
        points={[
          [centerX() + 100, centerY()],
          [centerX() + 300, centerY()]
        ]}
        stroke={'#64748b'}
        lineWidth={2}
        endArrow
        opacity={0}
      />

      <Line
        ref={arrow3}
        points={[
          [centerX() + 300, centerY() + 20],
          [centerX() + 100, centerY() + 20]
        ]}
        stroke={'#64748b'}
        lineWidth={2}
        endArrow
        opacity={0}
      />

      <Line
        ref={arrow4}
        points={[
          [centerX(), centerY() + 40],
          [centerX(), centerY() + 160]
        ]}
        stroke={'#64748b'}
        lineWidth={2}
        endArrow
        opacity={0}
      />

      <Line
        ref={arrow5}
        points={[
          [centerX(), centerY() + 240],
          [centerX(), centerY() + 310]
        ]}
        stroke={'#64748b'}
        lineWidth={2}
        endArrow
        opacity={0}
      />
    </Node>
  );

  // Animation sequence
  yield* waitFor(0.5);

  // Title
  yield* all(
    userInputBox().opacity(1, 0.8, easeOutCirc),
    userInputText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(0.5);

  // Show user input to Claude CLI flow
  yield* arrow1().opacity(1, 0.5, easeOutCirc);
  
  yield* waitFor(0.3);

  yield* all(
    claudeCliBox().opacity(1, 0.8, easeOutCirc),
    claudeCliText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(0.5);

  // Show Claude CLI to API communication
  yield* arrow2().opacity(1, 0.5, easeOutCirc);
  
  yield* waitFor(0.3);

  yield* all(
    anthropicApiBox().opacity(1, 0.8, easeOutCirc),
    anthropicApiText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(0.5);

  // Show response back
  yield* arrow3().opacity(1, 0.5, easeOutCirc);

  yield* waitFor(0.5);

  // Show tool execution
  yield* arrow4().opacity(1, 0.5, easeOutCirc);
  
  yield* waitFor(0.3);

  yield* all(
    toolsBox().opacity(1, 0.8, easeOutCirc),
    toolsText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(0.5);

  // Show TodoWrite
  yield* arrow5().opacity(1, 0.5, easeOutCirc);
  
  yield* waitFor(0.3);

  yield* all(
    todoWriteBox().opacity(1, 0.8, easeOutCirc),
    todoWriteText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(1);

  // Show all tool categories
  yield* all(
    coreFileOpsBox().opacity(1, 0.8, easeOutCirc),
    coreFileOpsText().opacity(1, 0.8, easeOutCirc),
    devToolsBox().opacity(1, 0.8, easeOutCirc),
    devToolsText().opacity(1, 0.8, easeOutCirc),
    webToolsBox().opacity(1, 0.8, easeOutCirc),
    webToolsText().opacity(1, 0.8, easeOutCirc),
    mcpBridgeBox().opacity(1, 0.8, easeOutCirc),
    mcpBridgeText().opacity(1, 0.8, easeOutCirc),
    mcpToolsBox().opacity(1, 0.8, easeOutCirc),
    mcpToolsText().opacity(1, 0.8, easeOutCirc),
    agentSystemBox().opacity(1, 0.8, easeOutCirc),
    agentSystemText().opacity(1, 0.8, easeOutCirc),
  );

  yield* waitFor(3);

  // Highlight key flow with pulsing
  yield* all(
    userInputBox().scale(1.1, 0.3),
    claudeCliBox().scale(1.1, 0.3),
    anthropicApiBox().scale(1.1, 0.3),
    toolsBox().scale(1.1, 0.3)
  );

  yield* all(
    userInputBox().scale(1, 0.3),
    claudeCliBox().scale(1, 0.3),
    anthropicApiBox().scale(1, 0.3),
    toolsBox().scale(1, 0.3)
  );

  yield* waitFor(2);
});