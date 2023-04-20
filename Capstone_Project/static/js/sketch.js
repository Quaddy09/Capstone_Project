paint = [];

// This is like pmouseX and pmouseY...but for every finger [pointer, middle, ring, pinky]
let prevPointer = [
  // Left hand
  [{x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}],
  // Right hand
  [{x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}, {x: 0, y: 0}]
];

// Landmark indexes for fingertips [pointer, middle, ring, pinky]...these are the same for both hands
let fingertips = [8, 12, 16, 20];


/**
 * Setup
 * - Configure handsfree
 * - Create start/stop buttons
 */
function setup () {
  let canvas = document.getElementById('gameDisplay');
  let x = canvas.offsetWidth;
  let y = canvas.offsetHeight;
  sketch = createCanvas(x, y);
  sketch.style('z-index', '1');
  sketch.parent('gameDisplay');

  // Colors for each fingertip
  colorMap = [
    // Left fingertips
    [color(0, 0, 0), color(255, 0, 255), color(0, 0, 255), color(255, 255, 255)],
    // Right fingertips
    [color(255, 0, 0), color(0, 255, 0), color(0, 0, 255), color(255, 255, 0)]
  ];

  // #1 Create HandsFree object & Turn on some models
  handsfree = new Handsfree({
    //showDebug: true, // Comment this out to hide the default webcam feed with landmarks
    hands: true
  });
  handsfree.enablePlugins('browser');
  handsfree.plugin.pinchScroll.disable();

  // Add webcam buttons under the canvas
  buttonStart = createButton('Start Webcam');
  buttonStart.id('start-webcam');
  buttonStart.class('handsfree-show-when-stopped');
  buttonStart.class('handsfree-hide-when-loading');
  buttonStart.mousePressed(() => handsfree.start());
  buttonStart.parent('gameDisplay');

  // Create a "loading..." button
  buttonLoading = createButton('...loading...');
  buttonLoading.class('handsfree-show-when-loading');
  buttonLoading.parent('gameDisplay');

  // Create a stop button
  buttonStop = createButton('Stop Webcam');
  buttonStart.id('stop-webcam');
  buttonStop.class('handsfree-show-when-started');
  buttonStop.mousePressed(() => handsfree.stop());
  buttonStop.parent('gameDisplay');
}

function windowResized() {
  window.location.reload();
}

/**
 * Main draw loop
 */
function draw () {
  background(0);
  fingerPaint();
  mousePaint();
  drawHands();
}

function fingerPaint () {
    // Canvas bounds to make drawing easier
    let bounds = document.querySelector('canvas').getClientRects()[0];
    // Check for pinches and create dots if something is pinched
    const hands = handsfree.data?.hands;

    // Paint with fingers
    if (hands?.pinchState) {
      // Loop through each hand
      hands.pinchState.forEach((hand, handIndex) => {
        // Loop through each finger
        hand.forEach((state, finger) => {
          if (hands.landmarks?.[handIndex]?.[fingertips[finger]]) {

            // Landmarks are in percentage, scale up
            let x = sketch.width - hands.landmarks[handIndex][fingertips[finger]].x * sketch.width;
            let y = hands.landmarks[handIndex][fingertips[finger]].y * sketch.height;

            // Start line on the spot that we pinched
            if (state === 'start') {
              prevPointer[handIndex][finger] = {x, y};

            // Add a line to the paint array
            } else if (state === 'held') {
              paint.push([
                prevPointer[handIndex][finger].x,
                prevPointer[handIndex][finger].y,
                x,
                y,
                colorMap[handIndex][finger]
              ]);
            }

            // Set the last position
            prevPointer[handIndex][finger] = {x, y};
          }
        })
      })
    }

    // Clear everything if the left [0] pinky [3] is pinched
    if (hands?.pinchState && hands.pinchState[0][3] === 'released') {
      paint = [];
    }

    // Draw Paint
    paint.forEach(p => {
      fill(p[4]);
      stroke(p[4]);
      strokeWeight(10);

      line(p[0], p[1], p[2], p[3]);
    })
  }



  /**
   * Draw the mouse
   */
  function mousePaint () {
    if (mouseIsPressed === true) {
      fill(colorMap[1][0]);
      stroke(colorMap[1][0]);
      strokeWeight(10);
      line(mouseX, mouseY, pmouseX, pmouseY);
    }
  }

  function drawHands () {
    const hands = handsfree.data?.hands;

    // Bail if we don't have anything to draw
    if (!hands?.landmarks) return;

    // Draw keypoints
    hands.landmarks.forEach((hand, handIndex) => {
      hand.forEach((landmark, landmarkIndex) => {
        // Set color
        if (colorMap[handIndex]) {
          switch (landmarkIndex) {
            case 8: fill(colorMap[handIndex][0]); break;
            case 12: fill(colorMap[handIndex][1]); break;
            case 16: fill(colorMap[handIndex][2]); break;
            case 20: fill(colorMap[handIndex][3]); break;
            default:
              fill(color(255, 255, 255));
          }
        }
        // Set stroke
        if (handIndex === 0 && landmarkIndex === 8) {
          stroke(color(255, 255, 255));
          strokeWeight(5);
          circleSize = 40;
        } else {
          stroke(color(0, 0, 0));
          strokeWeight(0);
          circleSize = 10;
        }

        circle(
          // Flip horizontally
          sketch.width - landmark.x * sketch.width,
          landmark.y * sketch.height,
          circleSize
        );
      })
    })
  }
