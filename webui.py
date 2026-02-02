import gradio as gr

# 占位的模型加载函数，仅用于展示接口形态，不实际下载权重

def load_model():
    """返回一个伪模型对象，在文案层面突出数据驱动视角。"""

    class DummyModel:
        def __call__(self, video_path: str, text_prompt: str):
            return {
                "recap": "【演示结果】本示例从数据采样与标注视角，对视频进行 Recap，突出 Tarsier2-Recap-585K 的设计思想。",
                "key_frames": [
                    "数据片段 A：覆盖高频动作模式的典型场景。",
                    "数据片段 B：刻画长距离时间依赖的复杂事件。",
                    "数据片段 C：补充少数类场景与极端条件。",
                ],
            }

    return DummyModel()


model = load_model()


def analyze_video(video, prompt):
    if video is None:
        return "请先上传一段用于数据分析示意的视频片段。", ["尚未检测到关键帧。"], ""

    outputs = model(str(video), prompt or "请从数据设计视角对该视频进行 Recap。")
    recap_text = outputs["recap"]
    key_frames = outputs["key_frames"]
    key_frames_markdown = "\n".join(f"- {item}" for item in key_frames)
    return recap_text, key_frames, key_frames_markdown


with gr.Blocks(title="Tarsier2-Recap-585K DataRecap WebUI（演示版）") as demo:

    gr.Markdown(
        """# Tarsier2-Recap-585K DataRecap WebUI（演示版）\n\n"
        "界面结构与主仓库一致，仅在说明文本中强调数据子集与标注策略。"""
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. 输入区：数据视角的视频样本")
            video_input = gr.Video(label="上传用于数据分析示意的视频", sources=["upload"], interactive=True)
            prompt_input = gr.Textbox(
                label="文本指令（可选）",
                value="请从数据分布与标注粒度的角度描述该视频。",
                lines=3,
            )
            run_btn = gr.Button("开始分析（演示，不进行真实推理）", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 2. 结果区：数据驱动的 Recap")
            recap_output = gr.Textbox(
                label="视频长篇描述（数据视角示意输出）",
                lines=10,
                interactive=False,
            )
            keyframe_gallery = gr.HighlightedText(
                label="关键片段（按数据角色划分）",
                combine_adjacent=True,
            )

    with gr.Accordion("可选：Markdown 结果导出", open=False):
        keyframe_md = gr.Markdown(
            "尚未检测到关键帧。可将伪结果复制至数据设计文档。"
        )

    def _wrapped_analyze(video, prompt):
        recap, key_frames, key_md = analyze_video(video, prompt)
        highlighted = [(kf, "关键片段") for kf in key_frames]
        return recap, highlighted, key_md

    run_btn.click(
        _wrapped_analyze,
        inputs=[video_input, prompt_input],
        outputs=[recap_output, keyframe_gallery, keyframe_md],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7862, show_error=True)
