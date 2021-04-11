import React, { createRef, RefObject } from "react";
import cfg from "./config";
import { eraseCanvasSubject, newDisplayImageSubject, newImageSubmissionSubject, newImageSubmittedSubject } from "./events";

export type Point = {
  x: number;
  y: number;
};

type DrawerState = {
  drawing: boolean;
  baseData: Array<any>;
};

type DrawerProps = {
  width?: number,
  height?: number
}

class Drawer extends React.Component<DrawerProps, DrawerState> {
  baseCanvasRef: RefObject<HTMLCanvasElement>;
  canvasRef: RefObject<HTMLCanvasElement>;
  ctx?: CanvasRenderingContext2D;

  constructor(props: any) {
    super(props);

    this.canvasRef = createRef<HTMLCanvasElement>();
    this.baseCanvasRef = createRef<HTMLCanvasElement>();
    this.state = { drawing: false, baseData: [] };
  }

  resetCanvasState() {
    if (this.ctx) {
      this.ctx.fillStyle = cfg.backgroundColor;
      this.ctx.fillRect(0, 0, 512, 512);
      this.ctx.lineWidth = cfg.lineWidth;
      this.ctx.strokeStyle = cfg.drawColor;
      this.ctx.lineJoin = "bevel";
      this.ctx.lineCap = "round";
    }
  }

  componentDidMount() {
    if (this.canvasRef.current) {
      this.ctx = this.canvasRef.current.getContext("2d") ?? undefined;

      if (this.ctx) {
        this.resetCanvasState();
      }

      if (this.baseCanvasRef.current) {
        const baseCtx = this.baseCanvasRef.current.getContext("2d");

        if (baseCtx) {
          baseCtx.fillStyle = cfg.backgroundColor;
          baseCtx.fillRect(0, 0, 512, 512);
          baseCtx.lineWidth = cfg.lineWidth;
          baseCtx.strokeStyle = cfg.drawColor;
          baseCtx.lineJoin = "bevel";
          baseCtx.lineCap = "round";
        }
      }

      this.canvasRef.current.onmousedown = (e: MouseEvent) =>
        this.onMouseDown(e);
      this.canvasRef.current.onmouseup = (e: MouseEvent) => this.onMouseUp(e);
      this.canvasRef.current.onmouseleave = (e: MouseEvent) =>
        this.onMouseLeave(e);
      this.canvasRef.current.onmousemove = (e: MouseEvent) =>
        this.onMouseMoved(e);
    }

    eraseCanvasSubject.subscribe(() => {
      this.ctx?.clearRect(0, 0, this.props.width || 512, this.props.height || 512);
      this.ctx?.fillRect(0, 0, this.props.width || 512, this.props.height || 512);
    })

    newDisplayImageSubject.subscribe(data => {
      if (this.ctx) {
        const dd = data as Array<any>;

        this.ctx.beginPath();
        this.ctx.moveTo(dd[0][0], dd[0][1]);
        dd.forEach((val: Array<any>, pIdx: number) => {
          val[0].forEach((pt: Array<any>, idx: number) => {
            this.ctx?.lineTo(val[0][idx], val[1][idx])
          })
        })
        this.ctx.closePath();
        this.ctx.stroke();
      }
    })

    newImageSubmissionSubject.subscribe(() => {
      if (this.canvasRef.current) {
        newImageSubmittedSubject.next(this.canvasRef.current.toDataURL());
      }
    })
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
      <div style={{position:'relative'}}>
        <canvas
          ref={this.canvasRef} 
          height={this.props.height} 
          width={this.props.width}
        >
        </canvas>
      </div>
    );
  }
}

export { Drawer };
