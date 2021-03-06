/*
Statement:

Given an input string, reverse the string word by word.

Example:
Input: "the sky is blue",
Output: "blue is sky the".
Note:

A word is defined as a sequence of non-space characters.

Input string may contain leading or trailing spaces. However,
your reversed string should not contain leading or trailing spaces.
You need to reduce multiple spaces between two words to a single
space in the reversed string.

Follow up: For C programmers, try to solve it in-place in O(1) space.

input: string
output: string, modified correctly so it is reversed and has no superfluous spaces


Compile with:
clang -std=c11 -g -Weverything -Werror 151-reverse-all-words-in-a-string.c -o ../../bin/151.bin

Test with:
tests/151-test.sh

----
Understand / Plan

We need to do three things to produce a correct answer:
- reverse the order of the words in the string
- remove unnecessary spaces between words
- remove trailing or leading spaces

We can accomplish this in these steps:
- strip leading spaces
- reverse the entire string
- re-reverse each word in the string to get correct ordering
- remove middle spaces with a constance space implementation
of memmove
- strip trailing whitespaces by moving null terminator up

Based on the problem boilerplate, we are going to assume that
the string is always null terminated.
----
Execute

See code below
----
Review:

Viewed the following discussions:
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static size_t left_shift_string(char *s, size_t len, size_t dst_i, size_t src_i)
{
  /*
  Given string s of length len, move the substring starting at index src_i to
  index dst_i, destructively overwriting a portion of the string. Appropriately moves
  (assumed-present) the null terminator, and returns the size of the shrunken string.
  Returns -1 on error.
  */

  if (src_i < dst_i)
  {
    //fprintf(stderr, "left_shift_string() | illegal src (%lu) and dst (%lu) indices; src must be greater than dst.\n", src_i, dst_i);
    return len;
  }

  if (!(((0 < src_i) && (src_i < len)) && ((0 <= dst_i) && (dst_i < len))))
  {
    //fprintf(stderr, "left_shift_string() | given src (%lu) and dst (%lu) would violate string boundaries.\n", src_i, dst_i);
    //fprintf(stderr, "left_shift_string() | %s. (%lu)\n", s, len);
    return len;
  }

  char *src_substr = s + (src_i * sizeof(char));
  char *dst_substr = s + (dst_i * sizeof(char));

  while (*src_substr != '\0')
  {
    *dst_substr = *src_substr;
    src_substr++;
    dst_substr++;
  }
  *dst_substr = '\0';

  return len - (src_i - dst_i);
}

static size_t strip_leading_spaces(char *s, size_t len)
{
  size_t true_start = 0;
  size_t i = 0;
  while (isspace(*(s + i)))
  {
    true_start++;
    i++;
  }

  size_t new_len = left_shift_string(s, len, 0, true_start);
  return new_len;
}

static size_t strip_middle_spaces(char *s, size_t len)
{
  size_t i = 0;
  while (s[i] != '\0' && i < len)
  {
    // Find first whitespace
    while (!(isspace(s[i])))
    {
      i++;
    }

    // Count following whitespaces, preserving one
    i++;
    size_t k = i;
    while (isspace(s[k]))
    {
      k++;
    }

    // Left shift substring to remove whitespace
    len = left_shift_string(s, len, i, k);
  }
  return len;
}

static size_t strip_trailing_spaces(char *const s, size_t len)
{
  while (isspace(*(s + len - 1)))
  {
    len--;
  }
  *(s + len) = '\0';
  return len;
}

static void reverse(char *const s, const size_t len)
{
  if (len == 0)
  {
    return;
  }

  size_t i = 0;
  size_t j = len - 1;
  char tmp = '\0';
  while (i < j)
  {
    //printf("Swapping s[%lu] (%c) and s[%lu] (%c) [len = %lu]\n", i, s[i], j, s[j], len);
    tmp = s[i];
    s[i] = s[j];
    s[j] = tmp;
    i++;
    j--;
  }
}

static void reverse_words(char *const s, const size_t len)
{
  for (size_t start = 0, end = 0; start < len;)
  {
    // find whitespace between words
    while (!(isspace(s[start + end]) || (s[start + end] == '\0')))
    {
      end++;
    }

    // Reverse word
    reverse(s + start, end);

    // Advance starting point, reset end
    start += end + 1;
    end = 0;
  }
}

static void reverseWords(char *s)
{
  size_t len = strlen(s);
  len = strip_leading_spaces(s, len);
  len = strip_trailing_spaces(s, len);
  len = strip_middle_spaces(s, len);
  reverse(s, len);
  reverse_words(s, len);
}

int main()
{
  size_t size;
  char *string = NULL;
  while (getline(&string, &size, stdin) != -1)
  {
    reverseWords(string);
    printf("%s\n", string);
  }

  free(string);
  return 0;
}
