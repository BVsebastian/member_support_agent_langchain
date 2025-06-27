# 📋 Coding Protocol

## 🎯 **Core Principles**

### **1. Write the Absolute Minimum Code Required**

- Implement only what's needed for the current task
- Avoid over-engineering or premature optimization
- Focus on functionality over perfection
- Get it working first, then improve

### **2. No Sweeping Changes**

- Make targeted, focused modifications
- Avoid refactoring unrelated code
- Preserve existing functionality
- Change only what's necessary

### **3. No Unrelated Edits - Focus on Just the Task You're On**

- Complete one subtask at a time
- Don't mix multiple features in one change
- Stay within the defined scope
- Resist the urge to "fix" other things

### **4. Make Code Precise, Modular, Testable**

- Single responsibility for each function/class
- Clear, descriptive naming
- Easy to test in isolation
- Modular design for reusability

### **5. Don't Break Existing Functionality**

- Test before and after changes
- Maintain backward compatibility
- Preserve existing APIs
- Ensure no regressions

---

## 🔄 **Implementation Process**

### **Step 1: Analyze Current State**

- Review existing code and documentation
- Understand what's already working
- Identify what needs to be added/modified
- Plan the minimal path forward

### **Step 2: Plan Minimal Changes**

- Break down into smallest possible subtasks
- Identify dependencies and order
- Plan the exact files and functions to modify
- Estimate effort and complexity

### **Step 3: Implement Focused Solution**

- Work on one subtask at a time
- Write minimal code to achieve the goal
- Follow existing patterns and conventions
- Add error handling where appropriate

### **Step 4: Test Functionality**

- Verify the change works as expected
- Test edge cases and error conditions
- Ensure no existing functionality is broken
- Document any issues found

### **Step 5: Update Documentation**

- Update task lists and progress
- Modify architecture documentation
- Add comments for complex logic
- Update any relevant README files

### **Step 6: Move to Next Subtask**

- Only proceed when current subtask is complete
- Maintain momentum without rushing
- Keep track of progress
- Celebrate small wins

---

## 📝 **Code Quality Standards**

### **Function Design**

- **Single Responsibility**: Each function does one thing well
- **Clear Naming**: Self-documenting function and variable names
- **Appropriate Size**: Functions should be readable in one screen
- **Error Handling**: Graceful handling of edge cases

### **Modularity**

- **Loose Coupling**: Minimize dependencies between modules
- **High Cohesion**: Related functionality grouped together
- **Reusability**: Design for reuse when appropriate
- **Testability**: Easy to test in isolation

### **Documentation**

- **Inline Comments**: Explain complex logic
- **Docstrings**: Document function purpose and parameters
- **README Updates**: Keep documentation current
- **Architecture Docs**: Maintain system overview

### **Testing**

- **Test Each Step**: Verify functionality before moving on
- **Edge Cases**: Consider error conditions
- **Integration**: Test how components work together
- **Regression**: Ensure existing features still work

---

## 🚫 **What to Avoid**

### **Anti-Patterns**

- ❌ **Big Bang Changes**: Don't rewrite everything at once
- ❌ **Scope Creep**: Don't add features not in the current task
- ❌ **Premature Optimization**: Don't optimize before it's working
- ❌ **Copy-Paste Code**: Don't duplicate without good reason
- ❌ **Magic Numbers**: Don't use unexplained constants

### **Process Anti-Patterns**

- ❌ **Skipping Tests**: Always test your changes
- ❌ **Ignoring Errors**: Handle errors gracefully
- ❌ **Breaking Changes**: Don't break existing functionality
- ❌ **Poor Documentation**: Keep docs updated

---

## ✅ **Success Criteria**

### **For Each Subtask**

- [ ] Functionality works as expected
- [ ] No existing functionality broken
- [ ] Code is readable and maintainable
- [ ] Error handling is appropriate
- [ ] Documentation is updated
- [ ] Tests pass (if applicable)

### **For Each Task**

- [ ] All subtasks completed
- [ ] Integration tested
- [ ] Documentation updated
- [ ] Ready for next task
- [ ] Commit message written

---

## 📚 **Examples**

### **Good Implementation**

```python
# ✅ Focused, minimal function
def get_user_name(user_id: str) -> str:
    """Get user name from database"""
    try:
        user = database.get_user(user_id)
        return user.name
    except UserNotFoundError:
        return "Unknown User"
```

### **Bad Implementation**

```python
# ❌ Too many responsibilities, no error handling
def process_user_data(user_id, update_profile, send_email, log_activity, validate_data):
    # 50 lines of mixed functionality
    pass
```

---

## 🎯 **Remember**

**The goal is to build incrementally, maintain quality, and avoid technical debt while making steady progress toward the final product.**

**When in doubt: Keep it simple, focused, and testable.**
