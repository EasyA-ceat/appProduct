"""
StateTracker 单元测试
"""
import os
import json
import pytest
from datetime import datetime, timedelta
from src.monitoring.state_tracker import StateTracker, TaskState, TaskStatus


class TestTaskStatus:

    def test_enum_values(self):
        """测试 TaskStatus 枚举值"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"


class TestStateTracker:

    def test_init(self, temp_dir):
        """测试初始化"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        assert tracker.tasks == {}
        assert tracker.start_time is None
        assert tracker.end_time is None

    def test_init_task(self, temp_dir):
        """测试初始化任务"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.init_task("research")
        
        assert "research" in tracker.tasks
        assert tracker.tasks["research"].status == TaskStatus.PENDING

    def test_start_task(self, temp_dir):
        """测试开始任务"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        tracker.init_task("research")
        
        tracker.start_task("research")
        
        assert tracker.tasks["research"].status == TaskStatus.IN_PROGRESS
        assert tracker.tasks["research"].start_time is not None

    def test_start_nonexistent_task(self, temp_dir):
        """测试开始未初始化的任务"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.start_task("nonexistent")
        
        assert "nonexistent" in tracker.tasks
        assert tracker.tasks["nonexistent"].status == TaskStatus.IN_PROGRESS

    def test_complete_task(self, temp_dir):
        """测试完成任务"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        tracker.init_task("research")
        tracker.start_task("research")
        
        tracker.complete_task("research")
        
        assert tracker.tasks["research"].status == TaskStatus.COMPLETED
        assert tracker.tasks["research"].end_time is not None
        assert tracker.tasks["research"].duration_seconds &gt;= 0

    def test_fail_task(self, temp_dir):
        """测试失败任务"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        tracker.init_task("research")
        tracker.start_task("research")
        
        error_msg = "网络连接失败"
        tracker.fail_task("research", error_msg)
        
        assert tracker.tasks["research"].status == TaskStatus.FAILED
        assert tracker.tasks["research"].error == error_msg

    def test_get_progress(self, temp_dir):
        """测试获取进度"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.init_task("task1")
        tracker.init_task("task2")
        tracker.init_task("task3")
        
        tracker.start_task("task1")
        tracker.complete_task("task1")
        tracker.start_task("task2")
        tracker.fail_task("task2", "error")
        
        progress = tracker.get_progress()
        
        assert progress == pytest.approx(66.666, rel=1e-3)

    def test_get_progress_no_tasks(self, temp_dir):
        """测试无任务时的进度"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        assert tracker.get_progress() == 0.0

    def test_start_and_end_workflow(self, temp_dir):
        """测试工作流开始和结束"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.start_workflow()
        assert tracker.start_time is not None
        
        tracker.end_workflow()
        assert tracker.end_time is not None

    def test_get_total_duration(self, temp_dir):
        """测试获取总时长"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.start_workflow()
        tracker.end_workflow()
        
        duration = tracker.get_total_duration()
        assert duration &gt;= 0

    def test_reset(self, temp_dir):
        """测试重置状态"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker = StateTracker(state_file)
        
        tracker.init_task("task1")
        tracker.start_workflow()
        tracker.save_state()
        
        assert os.path.exists(state_file)
        
        tracker.reset()
        
        assert tracker.tasks == {}
        assert tracker.start_time is None
        assert not os.path.exists(state_file)

    def test_save_and_load_state(self, temp_dir):
        """测试状态保存和加载"""
        state_file = os.path.join(temp_dir, "state.json")
        tracker1 = StateTracker(state_file)
        
        tracker1.init_task("research")
        tracker1.start_task("research")
        tracker1.complete_task("research")
        tracker1.save_state()
        
        # 加载到新的 tracker
        tracker2 = StateTracker(state_file)
        
        assert "research" in tracker2.tasks
        assert tracker2.tasks["research"].status == TaskStatus.COMPLETED
