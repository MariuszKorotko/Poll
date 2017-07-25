## Welcome to Poll Application

This basic poll application will consist of two parts:
- A public site that lets people view pools and vote in them.
- An admin site that lets add, change or delete polls.

### Models:
- Question contains fields: question and publication date:
  ```
    class Question(models.Model):
      question_text = models.CharField(max_length=256)
      pub_date = models.DateTimeField("date published")

      def __str__(self):
        return self.question_text

      def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
  ```
- Choice contains fields: the text of the choice and vote tally:
  ```
    class Choice(models.Model):
      question = models.ForeignKey(Question, on_delete=models.CASCADE)
      choice_text = models.CharField(max_length=256)
      votes = models.IntegerField(default=0)

      def __str__(self):
        return self.choice_text
  ```

### Views:
- Index display last five published questions (question_list.html):
  ```
    class IndexView(generic.ListView):
      context_object_name = 'latest_question_list'

      def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
  ```
- Detail display details of question (question_detail.html):
  ```
    class DetailView(generic.DetailView):
      model = Question
  ```
- Results display votes (results.html):
  ```
    class ResultsView(generic.DetailView):
      model = Question
      template_name = 'polls/results.html'
  ```
  - Vote view:
  ```
    def vote(request, question_id):
      question = get_object_or_404(Question, pk=question_id)

      try:
          selected_choice = question.choice_set.get(pk=request.POST['choice'])
      except (KeyError, Choice.DoesNotExist):
          # Redisplay the question voting form.
          return render(request, 'polls/question_detail.html',{
              'question': question,
              'error_message': "You didn't select a choice"
          })
      else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results',
                                                args=(question.id,)))
    ```

### Tests:
- Question model:
```
  def test_was_publised_recently_with_future_question(self):
      """
      was_published_recently() returns False for questions whose pub_date
      is in the future.
      """
      time = timezone.now() + datetime.timedelta(days=30)
      future_question = Question(pub_date=time)
      self.assertIs(future_question.was_published_recently(), False)

  def test_was_publised_recently_with_old_question(self):
      """
      was_published_recently() returns False for question whose pub_date
      is older than 1 day.
      """
      time = timezone.now() - datetime.timedelta(days=1, seconds=1)
      old_question = Question(pub_date=time)
      self.assertIs(old_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self):
      """
      was_published_recently() returns True for questions whose pub_date
      is within the last day.
      """
      time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                 seconds=59)
      recent_question = Question(pub_date=time)
      self.assertIs(recent_question.was_published_recently(), True)
```
