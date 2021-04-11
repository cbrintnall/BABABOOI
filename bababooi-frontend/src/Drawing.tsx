import React, { createRef, RefObject } from "react";
import cfg from "./config";

export type Point = {
  x: number;
  y: number;
};

type DrawerState = {
  drawing: boolean;
};

class Drawer extends React.Component<{}, DrawerState> {
  canvasRef: RefObject<HTMLCanvasElement>;
  ctx?: CanvasRenderingContext2D;

  constructor(props: any) {
    super(props);

    this.canvasRef = createRef<HTMLCanvasElement>();
    this.state = { drawing: false };
  }

  componentDidMount() {
    if (this.canvasRef.current) {
      this.ctx = this.canvasRef.current.getContext("2d") ?? undefined;

      if (this.ctx) {
        this.ctx.fillStyle = cfg.backgroundColor;
        this.ctx.fillRect(0, 0, 500, 500);
        this.ctx.lineWidth = cfg.lineWidth;
        this.ctx.strokeStyle = cfg.drawColor;
        this.ctx.lineJoin = "bevel";
        this.ctx.lineCap = "round";
      }

      this.canvasRef.current.onmousedown = (e: MouseEvent) =>
        this.onMouseDown(e);
      this.canvasRef.current.onmouseup = (e: MouseEvent) => this.onMouseUp(e);
      this.canvasRef.current.onmouseleave = (e: MouseEvent) =>
        this.onMouseLeave(e);
      this.canvasRef.current.onmousemove = (e: MouseEvent) =>
        this.onMouseMoved(e);
    }
  }

  getMouseCanvasPosition(e: MouseEvent): Point {
    const rect = this.canvasRef.current!.getBoundingClientRect();

    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
  }

  onMouseDown(e: MouseEvent) {
    this.setState({ drawing: true });

    this.startDrawing(this.getMouseCanvasPosition(e));
  }

  onMouseLeave(e: MouseEvent) {
    this.setState({ drawing: false });

    this.finishDrawing();
  }

  onMouseUp(e: MouseEvent) {
    this.setState({ drawing: false });

    this.finishDrawing();
  }

  startDrawing(mousePos: Point) {
    if (this.ctx) {
      this.ctx.beginPath();
      this.ctx.moveTo(mousePos.x, mousePos.y);
    }
  }

  finishDrawing() {
    if (this.ctx) {
      this.ctx.closePath();
    }
  }

  onMouseMoved(e: MouseEvent) {
    const canvasPos = this.getMouseCanvasPosition(e);

    if (this.ctx && this.state.drawing) {
      this.ctx.lineTo(canvasPos.x, canvasPos.y);
      this.ctx.stroke();
    }
  }

  render() {
    return (
      <div>
        <canvas ref={this.canvasRef} height={500} width={500}></canvas>
      </div>
    );
  }
}

export { Drawer };
