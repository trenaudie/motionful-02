import {makeScene2D, Txt} from '@motion-canvas/2d';
import {
  createRef,
  waitFor,
  easeOutCubic,
  createSignal,
} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  view.fill('#000000');

  const phrases = [
    "When you ask Claude CLI",
    "to 'fix this bug'...",
    "",
    "The request goes to",
    "Claude CLI (claude-code)",
    "",
    "Claude CLI communicates with",
    "Anthropic's API",
    "",
    "Claude receives your request",
    "and creates a response",
    "",
    "The response triggers",
    "tool execution",
    "",
    "Tools like Read, Edit,",
    "and Bash analyze and",
    "modify your code",
    "",
    "TodoWrite helps plan",
    "and track the work",
    "",
    "Supporting tools provide",
    "comprehensive capabilities:",
    "",
    "Core file operations,",
    "development tools, web tools",
    "",
    "MCP bridge connects to",
    "IDE diagnostics and",
    "code execution",
    "",
    "Agent system handles",
    "complex multi-step tasks"
  ];

  const textRef = createRef<Txt>();
  const textSignal = createSignal(0);

  // Create centered text element
  view.add(
    <Txt
      ref={textRef}
      text=""
      fontSize={64}
      fontFamily={'JetBrains Mono, Consolas, Monaco, monospace'}
      fontWeight={700}
      fill={'#ffffff'}
      opacity={() => textSignal()}
      x={0}
      y={0}
      textAlign={'center'}
      lineHeight={80}
      letterSpacing={2}
    />
  );

  // Animation sequence
  yield* waitFor(1);

  for (let i = 0; i < phrases.length; i++) {
    const phrase = phrases[i];
    
    // Skip empty phrases (used for spacing)
    if (phrase === "") {
      yield* waitFor(0.8);
      continue;
    }

    // Set the text
    textRef().text(phrase);
    
    // Fade in
    yield* textSignal(1, 0.6, easeOutCubic);
    
    // Hold the text
    yield* waitFor(2.5);
    
    // Fade out
    yield* textSignal(0, 0.4, easeOutCubic);
    
    // Short pause between phrases
    yield* waitFor(0.3);
  }

  // Final hold
  yield* waitFor(2);
});